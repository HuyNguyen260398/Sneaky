from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('C', 'COD'),
    ('B', 'Bank Transfer'),
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    country = CountryField(blank_label='(Select Country)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}))
    zip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Zip'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'}))
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'House number and street name'}))
    appartment_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Appartment, suite, unit etc: (optional)'}))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
