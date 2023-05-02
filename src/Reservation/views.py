import os.path

from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

from pathlib import Path

from Event.models import Representation, Event, Price
from Configuration.models import Place, Config
from .models import Reservation, Ticket, SeatingTicket, StandingTicket
from .forms import ReservationForm
from django.utils import timezone
from CollegeBook.settings import MEDIA_ROOT
from CollegeBook.utils import findRowId, findJsonID
import qrcode,json


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
    selected_seats = request.POST.getlist("selectedSeatsID[]")
    config = Config.objects.get(pk=Event.objects
                                .get(pk=Representation.objects.
                                     get(pk=representation_id).event.id).configuration.id)

    price = Place.objects.get(configuration=config, type="Classic").price
    total_price = len(selected_seats) * price

    return JsonResponse({'total_price': total_price, 'selected_seats': selected_seats})

def reserve_seats(request,representation_id):
    selectedSeatsIDs = request.POST.getlist("selectedSeatsIDs[]")
    rowOffset = 0
    url = request.POST.get("currentRoom")
    path = Path(__file__).resolve().parent.parent
    src_file = path.joinpath("Event" + url)
    with open(src_file,'r') as f:
        data = json.load(f)
    for seatID in selectedSeatsIDs:
        rowID = findRowId(seatID[0])
        rowID = rowID + rowOffset
        columnID = int(seatID[1:])
        while data[rowID]["class"] != "seat-row":
            rowID +=1
            rowOffset += 1
        jsonID = findJsonID(data[rowID]["seat"], columnID)
        if data[rowID]["seat"][jsonID] == "seat sold":
            seatsReserved = False
            return(JsonResponse({'seatsReserved': seatsReserved}))
        else:
            data[rowID]["seat"][jsonID] = "seat sold"
    with open(src_file,'w') as f:
        json.dump(data,f)
    seatsReserved = True
    return(JsonResponse({'seatsReserved': seatsReserved}))
    


def representation_reservation(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Event:display')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save(representation_id)

            return redirect('Payment:landing', form.instance.pk)

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
