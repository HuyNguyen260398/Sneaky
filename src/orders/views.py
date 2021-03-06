from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import ListView, DetailView, View

from .models import Order, ProductPurchase
from .forms import PaymentForm

from billing.models import BillingProfile
from carts.models import Cart


def payment_option_select(request):
    form = PaymentForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        payment_option = None
        _option = form.cleaned_data.get('payment_option')
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if billing_profile is not None:
            if _option == 'C':
                payment_option = "COD"
            elif _option == 'B':
                payment_option = "Bank Transfer"
            elif _option == 'S':
                payment_option = "Stripe"
            elif _option == 'P':
                payment_option = "Paypal"
            else:
                messages.warning(self.request, "Invalid payment option selected")
            order_obj.payment_option = payment_option
            order_obj.save()
            request.session['payment_option'] = payment_option
        else:
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)

    return redirect('cart:checkout')


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/orders-list.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order-detail.html"

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        raise Http404
