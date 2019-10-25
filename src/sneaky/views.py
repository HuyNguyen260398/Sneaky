from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import ContactForm

from products.models import Product, ProductVariant


def home_page(request):
    featured_products = Product.objects.featured()

    context = {
        'title': 'Home Page',
        'content': 'Welcome to the home page!',
        'featured_products': featured_products,
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'Premium Content!!!'
    return render(request, 'home.html', context)


def about_page(request):
    context = {
        'title': 'About Page',
        'content': 'Welcome to the about page!'
    }
    return render(request, 'about.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact Page',
        'content': 'Welcome to the contact page!',
        'form': contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({'message': 'Thank you for your submission!'})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'contact.html', context)
