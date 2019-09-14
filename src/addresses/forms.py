from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Address


class AddressForm(forms.ModelForm):
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

    class Meta:
        model = Address
        fields = [
            'country',
            'zip',
            'city',
            'street_address',
            'appartment_address',
        ]
