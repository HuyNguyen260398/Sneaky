import os
import random
import re
import decimal

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from sneaky.utils import unique_slug_generator, get_filename


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000000)
    name, ext = get_filename_ext(filename)
    final_filname = '{new_filename}{ext}'.format(
        new_filename=new_filename,
        ext=ext
    )
    return "products/{new_filename}/{final_filname}".format(
        new_filename=new_filename,
        final_filname=final_filname
    )


class ProductBrand(models.Model):
    brand = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand


def productbrand_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(productbrand_pre_save_receiver, sender=ProductBrand)


class ProductType(models.Model):
    type = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.type


def producttype_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(producttype_pre_save_receiver, sender=ProductType)


class ProductQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
        )
        return self.filter(lookups).distinct()

    # def filter(self, query):
    #     return self.all()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Can be used as Product.objects.featured
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    discount_percent = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=40.00)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, blank=True, null=True)

    objects = ProductManager()

    def get_absolute_url(self):
        first_variant = self.get_first_variant()
        return reverse('products:detail', kwargs={'slug': first_variant.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    @property
    def discount_price(self):
        return self.price - (self.discount_percent * self.price * decimal.Decimal(0.01))

    def get_variants(self):
        qs = self.productvariant_set.all()
        return qs

    def get_first_variant(self):
        qs = self.get_variants()[0]
        return qs

    def get_first_variant_img(self):
        qs = self.get_first_variant()
        img = qs.get_main_img()
        return img


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


class ProductColor(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def color(self):
        return self.title


def productcolor_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(productcolor_pre_save_receiver, sender=ProductColor)


class ProductSize(models.Model):
    title = models.CharField(max_length=10)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def size(self):
        return self.title


def productsize_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(productsize_pre_save_receiver, sender=ProductSize)


class ProductVariantQuerySet(models.QuerySet):
    def get_colors(self, product):
        qs = self.filter(product=product)
        color_list = qs.values_list('color', flat=True).distinct()
        unique_list = []
        for i in color_list:
            new_qs = qs.filter(color_id=i).first()
            unique_list.append(new_qs)
        return unique_list


class ProductVariantManager(models.Manager):
    def get_queryset(self):
        return ProductVariantQuerySet(self.model, using=self._db)

    def get_colors(self, product):
        return self.get_queryset().get_colors(product)


class ProductVariant(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)

    objects = ProductVariantManager()

    def __str__(self):
        return "{i}-{p}-{c}-{s}".format(i=self.id, p=self.product.id, c=self.color.title, s=self.size.title)

    @property
    def display_title(self):
        return "{p}-{c}-{s}".format(p=self.product.title, c=self.color.title, s=self.size.title)

    def get_absolute_url(self):
        first_variant = ProductVariant.objects.filter(
            product=self.product).filter(color=self.color)[0]
        return reverse('products:detail', kwargs={'slug': first_variant.slug})

    def get_add_to_cart_url(self):
        return reverse('cart:add-to-cart')

    def get_remove_from_cart_url(self):
        return reverse('cart:remove_from_cart', kwargs={'slug': self.slug})

    def get_increase_cart_url(self):
        return reverse('cart:increase_cart', kwargs={'slug': self.slug})

    def get_decrease_cart_url(self):
        return reverse('cart:decrease_cart', kwargs={'slug': self.slug})

    def get_imgs(self):
        qs = self.productimage_set.all()
        return qs

    def get_main_img(self):
        qs = self.get_imgs()[0]
        return qs


def productvariant_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(productvariant_pre_save_receiver, sender=ProductVariant)


class ProductImage(models.Model):
    productvariant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_image_path,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.name)

    def get_default_url(self):
        return self.productvariant.get_absolute_url()
