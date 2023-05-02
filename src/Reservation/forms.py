from django import forms

from Configuration.models import Place
from .models import Reservation, Representation, StandingTicket, SeatingTicket, DrinkTicket, FoodTicket


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'email',
            'last_name',
            'first_name',
            'phone',
            'note',
            'drink_number',
            'food_number'
        ]
        labels = {'email': 'Email', 'last_name': 'Nom', 'first_name': 'Prénom', 'phone': 'Numéro de téléphone',
                  'note': 'Commentaire', 'drink_number': 'Tickets boissons', 'food_number': 'Tickets nourriture'}
        widgets = {'drink_number': forms.NumberInput(attrs = {'min' : '0'}), 'food_number': forms.NumberInput(attrs={'min': '0'})}
        field_options = {'note': {'required': False}}
    selectedseat = forms.CharField(label='Place Selectionner', max_length=50, required=True)

    def save(self, representation_id, commit=True):
        reservation = super(ReservationForm, self).save(commit=False)
        if commit:
            reservation.representation = Representation.objects.get(pk=representation_id)
            reservation.save()
            for i in range(self.cleaned_data["drink_number"]):
                DrinkTicket.create(reservation_id=reservation.id)

            for j in range(self.cleaned_data["food_number"]):
                FoodTicket.create(reservation_id=reservation.id)

            selected_seats = self.cleaned_data["selectedseat"]
            selected_seats = selected_seats.split(",")
            for element in selected_seats:
                if element == "Debout":
                    place = Place.objects.get(type="Debout",
                                              configuration_id=reservation.representation.event.configuration_id)
                    StandingTicket.create(type_id=place.id, reservation_id=reservation.id)
                else:
                    # TODO changer le debout
                    place = Place.objects.get(type="Debout",
                                              configuration_id=reservation.representation.event.configuration_id)
                    SeatingTicket.create(seat_number=element, type_id=place.id, reservation_id=reservation.id)
        return reservation
