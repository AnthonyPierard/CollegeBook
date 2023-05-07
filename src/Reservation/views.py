from pathlib import Path

import json
import qrcode
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from unidecode import unidecode

from CollegeBook.utils import findRowId, findJsonID
from Configuration.models import Place, Config
from Event.models import Representation, Event, Price
from .forms import ReservationForm


def seat_selection(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Event:display')
    eventID = representation.event_id
    event = Event.objects.get(pk=eventID)
    configurationID = event.configuration_id
    configuration = Config.objects.get(pk=configurationID)
    url = "/static/json/" + unidecode(event.name) + "/" + str(representation.id) + ".json"


    places = Place.objects.filter(configuration_id=configurationID)
    seatTypes = [place.type for place in places]
    seatTypesJson = json.dumps(seatTypes)

    return render(request, 'seat_selection.html', {"representation": representation, "url": url, "seatTypes":seatTypesJson})


def process_price(request, representation_id):
    selected_seats_str = request.POST.get("selectedSeatsID")
    selected_seats = json.loads(selected_seats_str)
    config = Config.objects.get(pk=Event.objects
                                .get(pk=Representation.objects.
                                     get(pk=representation_id).event.id).configuration.id)
    total_price = 0
    for seatIDS in selected_seats:
        seatType = selected_seats[seatIDS].split()[1]
        price = Place.objects.get(configuration_id=config, type=seatType).price
        total_price += price

    return JsonResponse({'total_price': total_price, 'selected_seats': sorted(list(selected_seats.keys()))})

def reserve_seats(request,representation_id):
    selectedSeatsIDsSTR = request.POST.get("selectedSeatsIDs")
    roomType = request.POST.get("roomType")
    url = request.POST.get("currentRoom")

    seatsReserved = True
    selectedSeatsIDs = json.loads(selectedSeatsIDsSTR)
    if len(list(selectedSeatsIDs.keys())) == 0:
        seatsReserved = False
        return(JsonResponse({'seatsReserved': seatsReserved}))
    path = Path(__file__).resolve().parent.parent
    src_file = path.joinpath("Event" + url)

    with open(src_file,'r') as f:
        data = json.load(f)

    if roomType != "standing-zone" :
        rowOffset = 0
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
    
    else:
        remainingPlaces = data[0]["nbr_place"]
        for i in range(len(selectedSeatsIDs)):
            remainingPlaces -= 1
            if remainingPlaces == -1:
                seatsReserved = False
                return(JsonResponse({'seatsReserved': seatsReserved}))
        data[0]["nbr_place"] = remainingPlaces

    with open(src_file,'w') as f:
        json.dump(data,f)
    return(JsonResponse({'seatsReserved': seatsReserved}))
    


def representation_reservation(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Event:display')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        print("\n\n\n",form.is_valid())
        if form.is_valid():
            print("salut")
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
