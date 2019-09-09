from django import template

from carts.models import Cart

register = template.Library()


@register.filter
def cart_item_count(request):
    cart, new_cart = Cart.objects.new_or_get(request)
    return cart.get_cart_count()
