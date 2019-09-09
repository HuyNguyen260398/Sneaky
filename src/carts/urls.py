from django.urls import re_path, path

from .views import (
    cart_home,
    cart_update,
    add_to_cart,
    remove_from_cart,
    remove_item_from_cart,
    # checkout_home,
    # checkout_done_view,
)

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_item_from_cart/<slug:slug>/', remove_item_from_cart, name='remove_item'),
    # path('checkout/', checkout_home, name='checkout'),
    # path('checkout/succes', checkout_done_view, name='success'),
    path('update/', cart_update, name='update'),
]
