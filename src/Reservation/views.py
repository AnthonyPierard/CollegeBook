import os.path

from django.shortcuts import render, redirect

from Event.models import Representation, Event, Price
from Configuration.models import Place
from .models import Reservation, Ticket, SeatingTicket, StandingTicket
from .forms import ReservationForm
from CollegeBook.settings import MEDIA_ROOT

from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
import reportlab
import qrcode

def seat_selection(request, representation_id):
    representation = Representation.objects.get(pk = representation_id)
    return render(request, 'seat_selection.html', {"representation" : representation})

def representation_reservation(request, representation_id):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # reservation = Reservation()
            # reservation.email = form.cleaned_data['email']
            # reservation.last_name = form.cleaned_data["last_name"]
            # reservation.first_name = form.cleaned_data["first_name"]
            # reservation.phone = form.cleaned_data["phone"]
            # reservation.number = 1 #todo rendre l'incrémentation automatique
            # reservation.representation = Representation.objects.get(pk=representation_id)
            form.save(representation_id)

            reservation = Reservation.objects.filter(email= form.cleaned_data['email'], representation_id= representation_id).last()

            return redirect('Payment:landing', reservation.id)

    else:
        form = ReservationForm()
        event_id = Representation.objects.get(pk=representation_id).event
        price_tickets = Price.objects.filter(event=event_id)
        drink_price = price_tickets.get(type="Boisson")
        food_price = price_tickets.get(type="Nourriture")
        place_price = Place.objects.all()
        return render(request, 'representation_reservation.html',
                      {'form': form, 'drink_price': drink_price, 'food_price': food_price, "place_price": place_price})

def makeQrcode():
    data = 'https://www.youtube.com/shorts/SXHMnicI6Pg'
    img = qrcode.make(data)