import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from Reservation.models import Reservation, SeatingTicket, StandingTicket, Ticket
from Event.models import Place, Price
from CollegeBook.utils import stripe_id_creation

from .templates import *

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(id=self.kwargs["representation_id"])
        event_name = reservation.representation.event.name
        tickets = Ticket.objects.filter(reservation_id=reservation.id)
        tickets_quantity = dict()
        for ticket in tickets:
            if not ticket.type.type in tickets_quantity.keys():
                tickets_quantity[ticket.type.type] = 1
            else:
                tickets_quantity[ticket.type.type] += 1

        line_items = [{'price': stripe.Product.retrieve(stripe_id_creation(key, event_name))["default_price"], 'quantity':tickets_quantity[key]} for key in tickets_quantity.keys()]
        if reservation.drink_number > 0:
            line_items += [
                {
                    'price': stripe.Product.retrieve(stripe_id_creation("boisson", event_name))["default_price"],
                    'quantity': reservation.drink_number
                }
            ]
        if reservation.food_number > 0:
            line_items += [
                {
                    'price': stripe.Product.retrieve(stripe_id_creation("nourriture", event_name))["default_price"],
                    'quantity': reservation.food_number
                }
            ]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'bancontact', 'sepa_debit'],
            line_items= line_items,
            mode='payment',
            success_url= settings.DOMAIN + 'payment/success/',
            cancel_url= settings.DOMAIN + 'payment/cancel/',
        )
        return redirect(checkout_session.url)
    
def cancel(request):
    return render(request, 'cancel.html')

def success(request):
    return render(request, 'success.html')

def landing(request, representation_id):
    reservation = Reservation.objects.get(id=representation_id)

    standing_tickets = StandingTicket.objects.filter(reservation_id=reservation.id)
    standing_list = [{"type":ticket.type.type,  "price":ticket.type.price} for ticket in standing_tickets]
    seating_tickets = SeatingTicket.objects.filter(reservation_id=reservation.id)
    seating_list = [{"type":ticket.type.type, "place":ticket.seat_number, "price":ticket.type.price} for ticket in seating_tickets]
    drink_price = Price.objects.get(event_id=reservation.representation.event.id, type="Boisson").price
    food_price = Price.objects.get(event_id=reservation.representation.event.id, type="Nourriture").price
    price = 0
    for seat in standing_list + seating_list:
        price += seat["price"]
    price += reservation.food_number * food_price + reservation.drink_number * drink_price

    return render(request, 'landing.html', {"reservation":reservation, "standing_seats":standing_list, "seating_seats":seating_list, "price":price})