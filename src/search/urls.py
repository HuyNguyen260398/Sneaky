from django.urls import re_path, path

from .views import SearchProducView

app_name = 'search'

urlpatterns = [
    path('', SearchProducView.as_view(), name='query'),
]
