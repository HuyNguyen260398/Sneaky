from django_countries.fields import CountryField
from django.db import models

from billing.models import BillingProfile


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    street_address = models.CharField(max_length=120)
    appartment_addresss = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{country}\n{zip}\n{city}\n{street_address}\n{appartment_address}".format(
            country=self.country,
            zip=self.zip,
            city=self.city,
            street_address=self.street_address,
            appartment_address=self.appartment_addresss
        )
