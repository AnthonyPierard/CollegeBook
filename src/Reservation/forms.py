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
    selectedseat = forms.CharField(label='Place Selectionner', required=True)

    def save(self, representation_id, commit=True):
        reservation = super(ReservationForm, self).save(commit=False)
        if commit:
            reservation.representation = Representation.objects.get(pk=representation_id)
            reservation.save()
            if self.cleaned_data["drink_number"] > 0:
                DrinkTicket.create(reservation_id=reservation.id)
            if self.cleaned_data["food_number"] > 0:
                FoodTicket.create(reservation_id=reservation.id)

            selected_seats = self.cleaned_data["selectedseat"]
            selected_seats_dic = eval(selected_seats)
            # selected_seats = selected_seats.split(",")
            for element in selected_seats_dic.keys():
                type_siege = selected_seats_dic[element].split()[1]
                place = Place.objects.get(type= type_siege,
                                            configuration_id=reservation.representation.event.configuration_id)
                SeatingTicket.create(seat_number=element, type_id=place.id, reservation_id=reservation.id)
        return reservation 