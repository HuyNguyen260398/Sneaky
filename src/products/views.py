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
# from carts.models import Cart
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
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        # context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


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
    #     # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     # context['cart'] = cart_obj
    #     return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        try:
            instance = ProductVariant.objects.get(pk=pk)
        except ProductVariant.DoesNotExist:
            raise Http404('Not found...')
        except ProductVariant.MultipleObjectsReturned:
            qs = ProductVariant.objects.filter(pk=pk)
            instance = qs.first()
        except Exception:
            raise Http404('Uhhmm')

        return instance

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        qs = ProductVariant.objects.filter(pk=pk)
        if qs.count() < 1:
            raise Http404('Not found!')
        instance = qs.first()
        # product = Product.objects.filter(id=instance.id).first()
        # product_variants = product.get_variants()
        product_variants = ProductVariant.objects.filter(
            product=instance.product)
        imgs = instance.get_imgs()

        context['imgs'] = imgs
        context['variants'] = product_variants
        context['pk'] = pk
        return context


# class ProductDownloadView(View):
#     def get(self, request, *args, **kwargs):
#         slug = kwargs.get('slug')
#         pk = kwargs.get('pk')
#         downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
#         if downloads_qs.count() != 1:
#             raise Http404('Download not found!')
#         download_obj = downloads_qs.first()
#
#         can_download = False
#         user_ready = True
#         if download_obj.user_required:
#             if not request.user.is_authenticated:
#                 user_ready = False
#         purchased_products = Product.objects.none()
#         if download_obj.free:
#             can_download = True
#             user_ready = True
#         else:
#             purchased_products = ProductPurchase.objects.products_by_request(request)
#             if download_obj.product in purchased_products:
#                 can_download = True
#         if not can_download or not user_ready:
#             messages.error(request, "You do not have permission to download this item!")
#             return redirect(download_obj.get_default_url())
#
#         file_root = settings.PROTECTED_ROOT
#         filepath = download_obj.file.path
#         final_filepath = os.path.join(file_root, filepath)
#         filename = download_obj.display_name
#         final_filename = download_obj.get_filename(filepath, filename)
#
#         with open(final_filepath, 'rb') as f:
#             wrapper = FileWrapper(f)
#             mimetype = 'application/force-download'
#             guess_mimetype = guess_type(filepath)[0]
#             if guess_mimetype:
#                 mimetype = guess_mimetype
#                 response = HttpResponse(wrapper, content_type=mimetype)
#                 response['Content-Disposition'] = 'attachment;filename={}'.format(final_filename)
#                 response['X-SendFile'] = str(final_filename)
#
#             return response


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
