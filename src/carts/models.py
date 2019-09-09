from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.urls import reverse

from products.models import Product, ProductVariant


User = settings.AUTH_USER_MODEL


# class CartItemManager(models.Manager):
#     def new_or_get(self, request, product=None):
#         cart_item_id = request.session.get('cartitem_id', None)
#         qs = self.get_queryset().filter(id=cart_item_id)
#         if qs.count() == 1:
#             new_obj = False
#             cart_item_obj = qs.first()
#             if request.user.is_authenticated and cart_item_obj.user is None:
#                 cart_item_obj.user = request.user
#                 cart_item_obj.save()
#         else:
#             cart_item_obj = CartItem.objects.new(user=request.user, product=product)
#             new_obj = True
#             request.session['cart_item_obj'] = cart_item_obj.id
#         return cart_item_obj, new_obj
#
#     def new(self, user=None, product=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj = user
#         return self.model.objects.create(user=user_obj, product=product)


class CartItem(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # objects = CartItemManager()

    def __str__(self):
        return "{quantity} of {title}".format(quantity=self.quantity, title=self.product.title)

    def get_subtotal(self):
        return self.quantity * self.product.product.price


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,)
    items = models.ManyToManyField(CartItem, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def get_cart_count(self):
        cart_count = 0
        qs = self.items.all()
        for i in range(0, qs.count()):
            cart_count += qs[i].quantity
        return cart_count

    # @property
    # def is_digital(self):
    #     qs = self.products.all()
    #     new_qs = qs.filter(is_digital=False)
    #     if new_qs.exists():
    #         return False
    #     return True


# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action in ('post_add', 'post_remove', 'post_clear'):
#         products = instance.products.all()
#         total = 0
#         for x in products:
#             total += x.product.price
#         if instance.subtotal != total:
#             instance.subtotal = total
#             instance.save()


# m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08)
    else:
        instance.subtotal = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
