from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    # firstname = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': ''}))
    # lastname = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': ''}))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}))
    zip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'House number and street name'}))
    appartment_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Appartment, suite, unit etc: (optional)'}))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
