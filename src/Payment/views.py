import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from Reservation.models import Reservation, SeatingTicket, StandingTicket, Ticket
from Event.models import Place, Price
from CollegeBook.utils import stripe_id_creation

from .templates import *

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(id=self.kwargs["representation_id"])
        if reservation.paid:
            return redirect('Event:display')
            #TODO notif que c'est payé
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
        # if checkout_session_id == '' or stripe.checkout.Session.retrieve(checkout_session_id).status == "expired":
        if True:
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
        else:
            return redirect('Payment:cancel')
            #TODO error page
    
def cancel(request):
    return render(request, 'cancel.html')

def success(request):
    return render(request, 'success.html')

def landing(request, representation_id):
    reservation = Reservation.objects.get(id=representation_id)

    if reservation.paid:
        return redirect('Event:display')
        # TODO notif que c'est payé

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
        reservation = Reservation.objects.get(paid=False, checkout_session=event['data']['object']['id'])
        reservation.paid = True
        print(reservation)
        # email = EmailMessage(
        #     'Reservation',
        #     'Vous avez reserver un Ticket pour la representation de %s pour la date du %s' % (
        #     reservation.representation.event.name, reservation.representation.date),
        #     'collegebooktest@gmail.com',
        #     ['%s' % form.cleaned_data['email']],
        #     headers={"Reply-To": 'collegebooktest@gmail.com'})

        # selected_seats = form.cleaned_data["selectedseat"]
        # selected_seats = selected_seats.split(",")
        # prefix_mail = reservation.email.split("@")[0].replace('.', ' ')
        # date = str(reservation.representation.date).split(' ')[0]
        # qr_path = MEDIA_ROOT / 'QR'
        # ticket_path = MEDIA_ROOT / 'Ticket'
        # pdf_path = os.path.join(ticket_path, f'{date}_{prefix_mail}_Tickets.pdf')
        # if not os.path.exists(ticket_path):
        #     os.mkdir(ticket_path)
        # if not os.path.exists(qr_path):
        #     os.mkdir(qr_path)
        # p = canvas.Canvas(pdf_path)
        #
        # for i in range(len(selected_seats)):
        #     y = 150
        #     x = 50
        #     d = i + 1
        #     data = 'https://www.youtube.com/%d' % d
        #     img = qrcode.make(data)
        #     ticket_name = f'{date}_{prefix_mail}_Ticket_Place_{selected_seats[i]}.png'
        #     img.save(qr_path / ticket_name)
        #     p.drawString(x, y, "Tickets place %s" % selected_seats[i])
        #     y = + 200
        #     p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
        #     p.showPage()
        #
        # drink_number = int(form.cleaned_data["drink_number"])
        # if drink_number > 0:
        #     for i in range(drink_number):
        #         y = 150
        #         x = 50
        #         d = i + 1
        #         data = 'https://www.youtube.com/%d' % d
        #         img = qrcode.make(data)
        #         ticket_name = f'{date}_{prefix_mail}_Ticket_Boisson_n°{d}.png'
        #         img.save(qr_path / ticket_name)
        #         p.drawString(x, y, "Ticket Boisson")
        #         y = + 200
        #         p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
        #         p.showPage()
        #
        # food_number = int(form.cleaned_data["food_number"])
        # if food_number > 0:
        #     for i in range(food_number):
        #         y = 150
        #         x = 50
        #         d = i + 1
        #         data = 'https://www.youtube.com/%d' % d
        #         img = qrcode.make(data)
        #         ticket_name = f'{date}_{prefix_mail}_Ticket_Nourriture_n°{d}.png'
        #         img.save(qr_path / ticket_name)
        #         p.drawString(x, y, "Ticket Nourriture")
        #         y = + 200
        #         p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
        #         p.showPage()
        #
        # p.save()
        # email.attach_file(pdf_path)
        # email.send()
        # # email.attach_file('Tickets Nourriture n° %d.png' %d)

    return HttpResponse(status=200)