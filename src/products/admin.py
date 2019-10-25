from django.contrib import admin

from .models import (
    Product,
    ProductType,
    ProductBrand,
    ProductColor,
    ProductSize,
    ProductVariant,
    ProductImage
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    inlines = [ProductImageInline]

    class Meta:
        model = ProductVariant


class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "slug"]


admin.site.register(Product)

admin.site.register(ProductType)

admin.site.register(ProductBrand)

admin.site.register(ProductColor)

admin.site.register(ProductSize)

admin.site.register(ProductVariant, ProductAdmin)

admin.site.register(ProductImage)
