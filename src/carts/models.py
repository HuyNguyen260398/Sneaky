from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed, post_save
from django.urls import reverse

from products.models import Product, ProductVariant


User = settings.AUTH_USER_MODEL


class CartItem(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{quantity} of {title}".format(quantity=self.quantity, title=self.product.title)

    @property
    def subtotal(self):
        return self.quantity * self.product.product.discount_price


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

    @property
    def total(self):
        cart_items = self.items.all()
        total = 0
        for item in cart_items:
            total += item.subtotal
        return total
