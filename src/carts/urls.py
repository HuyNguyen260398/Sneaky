from django.urls import re_path, path

from .views import (
    cart_home,
    add_to_cart,
    remove_from_cart,
    increase_cart,
    decrease_cart,
    checkout_home,
    checkout_done_view,
    checkout,
)

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('increase_cart/<slug:slug>/', increase_cart, name='increase_cart'),
    path('decrease_cart/<slug:slug>/', decrease_cart, name='decrease_cart'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout2/', checkout, name='checkout2'),
    path('checkout/success/', checkout_done_view, name='success'),
]
