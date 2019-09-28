from django import forms

from .models import BillingProfile

PAYMENT_CHOICES = (
    ('C', 'COD'),
    ('B', 'Bank Transfer'),
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class PaymentForm(forms.Form):
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
