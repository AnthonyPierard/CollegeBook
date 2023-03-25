from django.shortcuts import render, redirect

from Event.models import Representation
from .models import Reservation
from .forms import ReservationForm


def seat_selection(request, representation_id):
    representation = Representation.objects.get(pk = representation_id)
    return render(request, 'seat_selection.html', {"representation" : representation})

def representation_reservation(request, representation_id):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = Reservation()
            reservation.email = form.cleaned_data['email']
            reservation.last_name = form.cleaned_data["last_name"]
            reservation.first_name = form.cleaned_data["first_name"]
            reservation.phone = form.cleaned_data["phone"]
            reservation.number = 1 #todo rendre l'incrémentation automatique
            reservation.representation = Representation.objects.get(pk=representation_id)

            reservation.save()
            return redirect('Event:display')

    else:
        form = ReservationForm()
    return render(request, 'representation_reservation.html', {'form': form})
