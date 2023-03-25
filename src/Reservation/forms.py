from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model =  Reservation
        fields = [
        'email',
        'last_name',
        'first_name',
        'phone'
        ]
        labels = {'email' : 'Email', 'last_name' : 'Nom', 'first_name' : 'Prénom', 'phone' : 'Numéro de téléphone'}