import os.path

from CollegeBook.utils import findRowId
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

from Event.models import Representation, Event, Price
from Configuration.models import Place, Config
from .models import Reservation, Ticket, SeatingTicket, StandingTicket
from .forms import ReservationForm
from django.utils import timezone
from CollegeBook.settings import MEDIA_ROOT

from reportlab.pdfgen import canvas
import reportlab, qrcode, json


def seat_selection(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Event:display')
    eventID = representation.event_id
    event = Event.objects.get(pk=eventID)
    configurationID = event.configuration_id
    configuration = Config.objects.get(pk=configurationID)
    url = "/static/json/" + event.name + "/" + str(representation.id) + ".json"
    return render(request, 'seat_selection.html', {"representation": representation, "url": url})


def process_price(request, representation_id):
    selected_seats = request.POST.getlist("selected_seats_ID[]")
    config = Config.objects.get(pk=Event.objects
                                .get(pk=Representation.objects.
                                     get(pk=representation_id).event.id).configuration.id)
    price = Place.objects.get(configuration=config, type="Classic").price
    total_price = len(selected_seats) * price

    return JsonResponse({'total_price': total_price, 'selected_seats': selected_seats})


def check_availability(request,representation_id):
    seatID = request.POST.get("seatID") 
    url = request.POST.get("currentRoom")
    with open(url,'r') as f:
        data = json.load(f)
    seatID_Json = findRowId(seatID[0])
        
def representation_reservation(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Event:display')
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

            reservation = Reservation.objects.filter(email=form.cleaned_data['email'],
                                                     representation_id=representation_id).last()

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
