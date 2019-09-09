from django.urls import re_path, path

from .views import (
    ProductDetailSlugView,
    # ProductDownloadView,
    ProductListView,
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    # re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail'),
    # re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
