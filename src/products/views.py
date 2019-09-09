from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper

# from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
# from orders.models import ProductPurchase

from .models import Product, ProductVariant


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
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().active()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'products/list.html', context)


class ProductDetailSlugView(DetailView):
    queryset = ProductVariant.objects.all()
    template_name = 'products/detail.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailSlugView, self).get_context_data(*args,
    #                                                                   **kwargs)
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     context['cart'] = cart_obj
    #     return context

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
        # pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        qs = ProductVariant.objects.all()
        this_instance = qs.filter(slug=slug)
        if this_instance.count() < 1:
            raise Http404('Not found!')
        instance = this_instance.first()
        # product = Product.objects.filter(id=instance.id).first()
        # product_variants = product.get_variants()
        colors = qs.get_colors(product=instance.product)
        sizes = qs.filter(product=instance.product).filter(color=instance.color)
        imgs = instance.get_imgs()

        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj

        context['imgs'] = imgs
        context['colors'] = colors
        context['sizes'] = sizes
        # context['pk'] = pk
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


def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('Product does not exist!')

    context = {
        'object': instance
    }
    return render(request, 'products/detail.html', context)
