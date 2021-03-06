from django.urls import re_path, path

from .views import (
    ProductDetailSlugView,
    # ProductDownloadView,
    ProductListView,
    ProductFilterView,
    products_api_list_view,
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('api/products/', products_api_list_view, name='products-api-list-view'),
    path('filter/', ProductFilterView.as_view(), name='filter-products'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail'),
    # re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
