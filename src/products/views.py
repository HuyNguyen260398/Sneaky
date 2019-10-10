from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper

# from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
# from orders.models import ProductPurchase

from .models import (
    Product,
    ProductVariant,
    ProductBrand,
    ProductType,
    ProductSize,
    ProductColor
)


class ProductFeatureListView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeatureDetailView(DetailView):
    template_name = 'products/featured-detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


# class UserProductHistoryView(LoginRequiredMixin, ListView):
#     template_name = 'products/user-history.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
#         return views


class ProductListView(ListView):
    model = Product
    paginate_by = 9
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        request = self.request

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        product_brands = ProductBrand.objects.all()
        product_types = ProductType.objects.all()
        product_sizes = ProductSize.objects.all()
        product_colors = ProductColor.objects.all()

        context['cart'] = cart_obj
        context['brands'] = product_brands
        context['types'] = product_types
        context['sizes'] = product_sizes
        context['colors'] = product_colors

        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        products = Product.objects.all()

        return products.order_by('id')


class ProductFilterView(ListView):
    model = ProductVariant
    paginate_by = 9
    template_name = 'products/filter.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFilterView, self).get_context_data(*args, **kwargs)
        request = self.request

        filtered_brand = request.GET.get('brandId', None)
        filtered_type = request.GET.get('typeId', None)
        filtered_size = request.GET.get('sizeId', None)
        filtered_color = request.GET.get('colorId', None)

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        product_brands = ProductBrand.objects.all()
        product_types = ProductType.objects.all()
        product_sizes = ProductSize.objects.all()
        product_colors = ProductColor.objects.all()

        context['cart'] = cart_obj
        context['brands'] = product_brands
        context['types'] = product_types
        context['sizes'] = product_sizes
        context['colors'] = product_colors
        context['filtered_brand'] = filtered_brand
        context['filtered_type'] = filtered_type
        context['filtered_size'] = filtered_size
        context['filtered_color'] = filtered_color

        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        product_variants = ProductVariant.objects.all()

        filtered_brand = request.GET.get('brandId', None)
        filtered_type = request.GET.get('typeId', None)
        filtered_size = request.GET.get('sizeId', None)
        filtered_color = request.GET.get('colorId', None)

        if filtered_brand is not None and filtered_brand != 'undefined':
            product_variants = product_variants.filter(product__brand__id=filtered_brand)
        if filtered_type is not None and filtered_type != 'undefined':
            product_variants = product_variants.filter(product__type__id=filtered_type)
        if filtered_size is not None and filtered_size != 'undefined':
            product_variants = product_variants.filter(size__id=filtered_size)
        if filtered_color is not None and filtered_color != 'undefined':
            product_variants = product_variants.filter(color__id=filtered_color)

        return product_variants.order_by('id')


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
    }
    return render(request, 'products/list.html', context)


class ProductDetailSlugView(DetailView):
    queryset = ProductVariant.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = ProductVariant.objects.get(slug=slug)
        except ProductVariant.DoesNotExist:
            raise Http404('Not found...')
        except ProductVariant.MultipleObjectsReturned:
            qs = ProductVariant.objects.filter(slug=slug)
            instance = qs.first()
        except Exception:
            raise Http404('Uhhmm')

        return instance

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug')
        qs = ProductVariant.objects.all()
        this_instance = qs.filter(slug=slug)
        if this_instance.count() < 1:
            raise Http404('Not found!')
        instance = this_instance.first()
        colors = qs.get_colors(product=instance.product)
        sizes = qs.filter(product=instance.product).filter(color=instance.color)
        imgs = instance.get_imgs()

        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['imgs'] = imgs
        context['colors'] = colors
        context['sizes'] = sizes
        return context


class ProductDetailView(DetailView):
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk)
        first_variant = product.get_first_variant()
        context['first_variant'] = first_variant
        return context

    def get_queryset(self, *args, **kwargs):
        # request = self.request
        pk = self.kwargs.get('pk')
        return ProductVariant.objects.filter(pk=pk)
