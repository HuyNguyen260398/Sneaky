from django.urls import re_path, path

from .views import (
    ProductDetailSlugView,
    # ProductDownloadView,
    ProductListView,
    ProductFilterView,
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('filter/', ProductFilterView.as_view(), name='filter-products'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail'),
    # re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
