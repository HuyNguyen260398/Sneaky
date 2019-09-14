from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import BillingProfile, Card

import stripe

STRIPE_SEC_KEY = getattr(settings, "STRIPE_SEC_KEY", "sk_test_L2UkxaY9kJLqL3veVS0fCuLv00uVo6w8I4")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_8hljcboVHoSIRIswWFCEwlIY00Xdsw19Ue")

stripe.api_key = STRIPE_SEC_KEY


def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart/")

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': 'Cannot find this user!'}, status_code=401)

        token = request.POST.get('token')
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
            return JsonResponse({'message': 'Success! Your casd was added.'})
    return HttpResponse("error", status_code=401)
