import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from Reservation.models import Ticket
from Event.models import Place

from .templates import *

stripe.api_key = settings.STRIPE_SECRET_KEY

# stripe.Price.create(product='test', unit_amount= 200, currency='eur')
stripe.Product.create(
    name='test_product',
    default_price_data={
        'unit_amount': 200,
        'currency':'eur'
    },
    expand=['default_price'],
)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        id = Place.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'bancontact', 'sepa_debit'],
            line_items=[
                {
                    # 'price_data':{
                    #     'currency':'eur',
                    #     'product':'classicDanseCanard',
                    #     'unit_amount': 200
                    # },
                    'price': stripe.Product.retrieve('classicDanseCanard')["default_price"],
                    'quantity': 2
                },
            ],
            mode='payment',
            success_url= settings.DOMAIN + 'payment/success/',
            cancel_url= settings.DOMAIN + 'payment/cancel/',
        )
        return redirect(checkout_session.url)
    
def cancel(request):
    return render(request, 'cancel.html')

def success(request):
    return render(request, 'success.html')

def ProductLandingPageView(request):
    place = Place.objects.get(type="classicq")
    return render(request, 'landing.html', {'place': place})