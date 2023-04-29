from django import forms

from .models import Reservation, Representation, Place, Price, StandingTicket, SeatingTicket


class ReservationForm(forms.ModelForm):
    class Meta:
        model =  Reservation
        fields = [
        'email',
        'last_name',
        'first_name',
        'phone',
        'note',
        'drink_number',
        'food_number'
        ]
        labels = {'email' : 'Email', 'last_name' : 'Nom', 'first_name' : 'Prénom', 'phone' : 'Numéro de téléphone', 'note': 'Commentaire', 'drink_number': 'Tickets boissons', 'food_number': 'Tickets nourriture'}
        widgets = {'drink_number': forms.NumberInput, 'food_number': forms.NumberInput}

    selectedseat = forms.CharField(label='Place Selectionner', max_length=50, required=True)

    def save(self, representation_id, commit=True):
        reservation = super(ReservationForm, self).save(commit=False)
        if commit:
            reservation.representation = Representation.objects.get(pk=representation_id)
            reservation.save()

            selected_seats = self.cleaned_data["selectedseat"]
            selected_seats = selected_seats.split(",")
            for element in selected_seats:
                if element == "Debout":
                    print(reservation.representation.event_id)
                    place = Place.objects.get(type="Debout", event_id=reservation.representation.event_id)
                    StandingTicket(type_id = place.id, reservation_id = reservation.id).save()
                else:
                    #TODO changer le debout
                    place = Place.objects.get(type="Debout", event_id=reservation.representation.event_id)
                    SeatingTicket(seat_number= element, type_id= place.id, reservation_id = reservation.id).save()
        return reservation