from django.urls import re_path, path

from .views import (
    AccountHomeView,
    AccountEmailActivateView,
    UserDetailUpdateView,
)

# from products.views import UserProductHistoryView

app_name = 'account'

urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    path('details/', UserDetailUpdateView.as_view(), name='user-update'),
    # re_path(r'^history/products/$', UserProductHistoryView.as_view(), name='user-product-history'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
            AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/',
         AccountEmailActivateView.as_view(), name='resend-activation'),
]
