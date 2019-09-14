from django.urls import re_path, path

from .views import (
    cart_home,
    # cart_update,
    add_to_cart,
    remove_from_cart,
    increase_cart,
    decrease_cart,
    CheckoutView,
    checkout_home,
    # checkout_done_view,
)

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('increase_cart/<slug:slug>/', increase_cart, name='increase_cart'),
    path('decrease_cart/<slug:slug>/', decrease_cart, name='decrease_cart'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/', checkout_home, name='checkout'),
    # path('checkout/succes', checkout_done_view, name='success'),
    # path('update/', cart_update, name='update'),
]
