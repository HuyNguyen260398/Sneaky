from django.views.generic import ListView

from products.models import (
    Product,
    ProductBrand,
    ProductType,
    ProductSize,
    ProductColor
)


class SearchProducView(ListView):
    template_name = 'search/view.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProducView, self).get_context_data(
            *args,
            **kwargs
        )
        query = self.request.GET.get('q')
        product_brands = ProductBrand.objects.all()
        product_types = ProductType.objects.all()
        product_sizes = ProductSize.objects.all()
        product_colors = ProductColor.objects.all()

        context['query'] = query
        context['brands'] = product_brands
        context['types'] = product_types
        context['sizes'] = product_sizes
        context['colors'] = product_colors
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)  # Same as method_dict['q']

        if query is not None:
            return Product.objects.search(query)

        return Product.objects.all()
