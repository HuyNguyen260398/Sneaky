import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm

from accounts.models import GuestEmail
from addresses.models import Address
from billing.models import BillingProfile
from products.models import Product, ProductVariant
from orders.models import Order

from .forms import CheckoutForm
from .models import Cart, CartItem

STRIPE_SEC_KEY = getattr(settings, "STRIPE_SEC_KEY", "sk_test_L2UkxaY9kJLqL3veVS0fCuLv00uVo6w8I4")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_8hljcboVHoSIRIswWFCEwlIY00Xdsw19Ue")

stripe.api_key = STRIPE_SEC_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'id': x.id,
        'url': x.get_absolute_url(),
        'image': x.get_main_img.image.url(),
        'name': x.product.title,
        'price': x.product.price
    } for x in cart_obj.products.all()]
    cart_data = {'products': products, 'subtotal': cart_obj.subtotal, 'total': cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/cart.html', {'cart': cart_obj})


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    color_id = request.POST.get('color_id')
    size_id = request.POST.get('size_id')

    # product = get_object_or_404(ProductVariant, slug=product_slug)
    product_qs = ProductVariant.objects.filter(
        product__id=product_id, color__id=color_id, size__id=size_id)
    if product_qs.exists():
        product = product_qs.first()
        cart, new_cart = Cart.objects.new_or_get(request)

        item_qs = cart.items.filter(product__id=product.id)
        if item_qs.exists():
            cart_item = item_qs[0]
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(product=product)
            cart.items.add(cart_item)

        if request.is_ajax():
            json_data = {
                'cartItemCount': cart.get_cart_count(),
            }
            return JsonResponse(json_data, status=200)
    return redirect('cart:home')


def remove_from_cart(request, slug):
    product = get_object_or_404(ProductVariant, slug=slug)
    if product is not None:
        cart, new_cart = Cart.objects.new_or_get(request)
        item_qs = cart.items.filter(product__slug=product.slug)
        if item_qs.exists():
            cart_item = item_qs[0]
            cart.items.remove(cart_item)
    return redirect('cart:home')


def increase_cart(request, slug):
    product = get_object_or_404(ProductVariant, slug=slug)
    if product is not None:
        cart, new_cart = Cart.objects.new_or_get(request)
        item_qs = cart.items.filter(product__slug=product.slug)
        if item_qs.exists():
            cart_item = item_qs[0]
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(product=product)
            cart.items.add(cart_item)
    return redirect('cart:home')


def decrease_cart(request, slug):
    product = get_object_or_404(ProductVariant, slug=slug)
    if product is not None:
        cart, new_cart = Cart.objects.new_or_get(request)
        item_qs = cart.items.filter(product__slug=product.slug)
        if item_qs.exists():
            cart_item = item_qs[0]
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.remove(cart_item)
    return redirect('cart:home')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "carts/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            city = form.cleaned_data.get('city')
            street_address = form.cleaned_data.get('street_address')
            appartment_address = form.cleaned_data.get('appartment_address')
            same_billing_address = form.cleaned_data.get('same_billing_address')
            save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')

            billing_address = BillingAddress(
                user=self.request.user,
                country=country,
                zip=zip,
                city=city,
                street_address=street_address,
                appartment_address=appartment_address,
                same_billing_address=same_billing_address,
                save_info=save_info,
                payment_option=payment_option,
            )
            billing_address.save()
            return redirect('cart:checkout')
        return redirect('cart:checkout')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.items.count() == 0:
        return redirect('cart:home')

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    # print(request)
    address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_address_id = request.session.get('billing_address_id', None)
    # shipping_address_required = not cart_obj.is_digital
    address_qs = None
    has_card = False

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect('cart:success')
            else:
                return redirect('cart:checkout')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        'has_card': has_card,
        'publish_key': STRIPE_PUB_KEY,
        # 'shipping_address_required': shipping_address_required,
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
