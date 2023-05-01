import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from Reservation.models import Reservation, SeatingTicket, StandingTicket, Ticket, AbstractTicket, FoodTicket, DrinkTicket
from Event.models import Price
from CollegeBook.utils import stripe_id_creation, create_ticket_pdf
from CollegeBook.settings import MEDIA_ROOT
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
import reportlab
import qrcode
import os
from unidecode import unidecode
from .templates import *

stripe.api_key = settings.STRIPE_SECRET_KEY

#TODO empêcher d'accéder à certaines pages
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(id=self.kwargs["representation_id"])
        if reservation.paid:
            return redirect('Payment:paid')
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

        checkout_session_id = reservation.checkout_session
        if checkout_session_id == '' or stripe.checkout.Session.retrieve(checkout_session_id).status == "expired":
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'bancontact', 'sepa_debit'],
                line_items= line_items,
                mode='payment',
                success_url= settings.DOMAIN + 'payment/success/',
                cancel_url= settings.DOMAIN + 'payment/cancel/',
            )
            reservation.checkout_session = checkout_session.id
            reservation.save()

        else:
            checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        if checkout_session.status == "open":
            return redirect(checkout_session.url)
        elif checkout_session.status == "complete":
            return render(request, 'paid.html')
        else:
            return render(request, '404.html')
    
def cancel(request):
    return render(request, 'cancel.html')

def success(request):
    return render(request, 'success.html')

def paid(request):
    return render(request, 'paid.html')

def landing(request, representation_id):
    reservation = Reservation.objects.get(id=representation_id)

    if reservation.paid:
        return redirect('Payment:paid')

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

@csrf_exempt
def webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # print(event)
        # session = stripe.checkout.Session.retrieve(
        #     event['data']['object']['id']
        # )
        # print(session)
        reservation = Reservation.objects.get(checkout_session=event['data']['object']['id'])
        reservation.paid = True
        reservation.save()
        date = str(reservation.representation.date).split(' ')[0]
        email = EmailMessage(
            'Reservation',
            'Vous avez reserver un Ticket pour la representation de %s pour la date du %s' % (
            reservation.representation.event.name, date),
            'collegebooktest@gmail.com',
            ['%s' % reservation.email],
            headers={"Reply-To": 'collegebooktest@gmail.com'})

        selected_seats = [ ticket.seat_number for ticket in Ticket.objects.filter(reservation_id=reservation.id) ]
        prefix_mail = reservation.email.split("@")[0].replace('.', ' ')
    
        qr_path = MEDIA_ROOT / 'QR'
        ticket_path = MEDIA_ROOT / 'Ticket'
        pdf_path = os.path.join(ticket_path, f'{date}_{prefix_mail}_Tickets.pdf')
        if not os.path.exists(ticket_path):
            os.mkdir(ticket_path)
        if not os.path.exists(qr_path):
            os.mkdir(qr_path)
        pdf = canvas.Canvas(pdf_path)
        print("here1")
        
        seating_tickets = SeatingTicket.objects.filter(reservation = reservation)
        standing_tickets = StandingTicket.objects.filter(reservation = reservation)
        food_tickets = FoodTicket.objects.filter(reservation = reservation)
        drink_tickets = DrinkTicket.objects.filter(reservation = reservation)
        
        for ticket in seating_tickets:
            code = ticket.code 
            trigramme = ticket.seat_number
            pdf = create_ticket_pdf(pdf, trigramme, code,  reservation.first_name,reservation.last_name,reservation.representation.event.name,reservation.representation.date)

        for ticket in standing_tickets:
            code = ticket.code 
            pdf = create_ticket_pdf(pdf, "Debout", code,  reservation.first_name,reservation.last_name,reservation.representation.event.name,reservation.representation.date)
        
        for ticket in food_tickets:
            code = ticket.code 
            pdf = create_ticket_pdf(pdf, "Nourriture", code,  reservation.first_name,reservation.last_name,reservation.representation.event.name,reservation.representation.date)

        for ticket in drink_tickets:
            code = ticket.code 
            pdf = create_ticket_pdf(pdf, "Boisson", code,  reservation.first_name,reservation.last_name,reservation.representation.event.name,reservation.representation.date)
            
        pdf.save()
        email.attach_file(pdf_path)
        email.send()
       
        print("mail send")
    return HttpResponse(status=200)