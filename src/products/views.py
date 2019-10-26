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


def products_api_list_view(request):
    products_json_list = [{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'product': p.product.title,
        'type': p.product.type.title,
        'brand': p.product.brand.title,
        'color': p.color.title,
        'size': p.size.title,
        'gender': p.product.gender,
        'price': p.product.price,
    } for p in ProductVariant.objects.all()]
    products_data = {'products': products_json_list}
    return JsonResponse(products_data)


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

        product_genders = {
            '1': 'Men',
            '2': 'Women',
            '3': 'Boys',
            '4': 'Girls',
        }

        product_prices = {
            '1': 'Under $100',
            '2': '$100 - $300',
            '3': '$300 - $500',
            '4': '$500 - $700',
            '5': '$700 - $900',
            '6': 'Above $900',
        }

        context['cart'] = cart_obj
        context['brands'] = product_brands
        context['types'] = product_types
        context['genders'] = product_genders
        context['sizes'] = product_sizes
        context['colors'] = product_colors
        context['prices'] = product_prices

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
        filtered_gender = request.GET.get('genderId', None)
        filtered_size = request.GET.get('sizeId', None)
        filtered_color = request.GET.get('colorId', None)
        filtered_price = request.GET.get('priceId', None)

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        product_brands = ProductBrand.objects.all()
        product_types = ProductType.objects.all()
        product_sizes = ProductSize.objects.all()
        product_colors = ProductColor.objects.all()

        product_genders = {
            '1': 'Men',
            '2': 'Women',
            '3': 'Boys',
            '4': 'Girls',
        }

        product_prices = {
            '1': 'Under $100',
            '2': '$100 - $300',
            '3': '$300 - $500',
            '4': '$500 - $700',
            '5': '$700 - $900',
            '6': 'Above $900',
        }

        context['cart'] = cart_obj
        context['brands'] = product_brands
        context['types'] = product_types
        context['genders'] = product_genders
        context['sizes'] = product_sizes
        context['colors'] = product_colors
        context['prices'] = product_prices
        context['filtered_brand'] = filtered_brand
        context['filtered_type'] = filtered_type
        context['filtered_gender'] = filtered_gender
        context['filtered_size'] = filtered_size
        context['filtered_color'] = filtered_color
        context['filtered_price'] = filtered_price

        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        product_variants = ProductVariant.objects.all()

        filtered_brand = request.GET.get('brandId', None)
        filtered_type = request.GET.get('typeId', None)
        filtered_gender = request.GET.get('genderId', None)
        filtered_size = request.GET.get('sizeId', None)
        filtered_color = request.GET.get('colorId', None)
        filtered_price = request.GET.get('priceId', None)

        product_genders = {
            '1': 'men',
            '2': 'women',
            '3': 'boys',
            '4': 'girls',
        }

        product_prices = {
            '1': 'Under $100',
            '2': '$100 - $300',
            '3': '$300 - $500',
            '4': '$500 - $700',
            '5': '$700 - $900',
            '6': 'Above $900',
        }

        if filtered_brand is not None and filtered_brand != 'undefined':
            product_variants = product_variants.filter(product__brand__id=filtered_brand)
        if filtered_type is not None and filtered_type != 'undefined':
            product_variants = product_variants.filter(product__type__id=filtered_type)
        if filtered_gender is not None and filtered_gender != 'undefined':
            product_variants = product_variants.filter(
                product__gender=product_genders[filtered_gender])
        if filtered_size is not None and filtered_size != 'undefined':
            product_variants = product_variants.filter(size__id=filtered_size)
        if filtered_color is not None and filtered_color != 'undefined':
            product_variants = product_variants.filter(color__id=filtered_color)
        if filtered_price is not None and filtered_price != 'undefined':
            if product_prices[filtered_price] == 'Under $100':
                product_variants = product_variants.filter(product__price__lte=100)
            elif product_prices[filtered_price] == '$100 - $300':
                product_variants = product_variants.filter(product__price__range=(100, 300))
            elif product_prices[filtered_price] == '$300 - $500':
                product_variants = product_variants.filter(product__price__range=(300, 500))
            elif product_prices[filtered_price] == '$500 - $700':
                product_variants = product_variants.filter(product__price__range=(500, 700))
            elif product_prices[filtered_price] == '$700 - $900':
                product_variants = product_variants.filter(product__price__range=(700, 900))
            elif product_prices[filtered_price] == 'Above $900':
                product_variants = product_variants.filter(product__price__gt=900)

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
        related_products = Product.objects.filter(
            brand=instance.product.brand).exclude(id=instance.product.id)[:4:]
        if related_products.count() < 1:
            related_products = Product.objects.all()[:4:]

        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['imgs'] = imgs
        context['colors'] = colors
        context['sizes'] = sizes
        context['related_products'] = related_products
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
