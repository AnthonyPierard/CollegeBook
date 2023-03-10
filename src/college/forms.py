from django import forms
from django.core import validators
from .utils import check_password

from .models import Evenement, Representation, User, Reservation
from datetime import datetime
import json



class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff',
        ]
        labels = {'first_name': 'Prenom','last_name':'Nom','email':'Email', 'password':'Password','is_staff':'Super Admin'}
        widgets = {'password': forms.PasswordInput}
    # pseudo = forms.CharField(label='Pseudonyme',max_length=50, required = True)
    # password = forms.CharField(label='Password', max_length=50, required = True, widget = forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=50, required = True, widget = forms.PasswordInput)
    # is_super = forms.BooleanField(label='Super Admin', required=False)
    def clean_confirm_password(self):
        check_password(self)

    def save(self, commit=True):
        user = super(AdminForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',

        ]
        labels = {'first_name': 'Prenom','last_name':'Nom','email':'Email'}

class LoginAdminForm(forms.Form):
    email = forms.CharField(label='Email', max_length=50, required = True)
    password = forms.CharField(label='Password', max_length=50, required = True, widget = forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = [
            'even_nom',
            'even_illustration',
            'even_description',
            'even_duree',
            #'event_time',
            'configuration_salle',
            'admin'

            #'can_moderate',
            #'promo_code'

            
        ]
        lables = {'event_nom' : 'Nom','even_duree':'Durée','even_description': 'desc', 'even_illustration':'illus','configuration_salle':'conf', 'admin':'Organisateurs'}

    date = forms.CharField(widget=forms.TextInput(attrs={'class':'MultiDate'}))
    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)

        if commit:
            event.save()
            for admin in self.cleaned_data["admin"]:
                event.admin.add(admin)
            dates = self.cleaned_data['date'].split(', ')
            if dates != '':
                event = Evenement.objects.get(even_nom=self.cleaned_data['even_nom'])
                for date in dates:
                    test = datetime.strptime(date, '%d-%m-%Y/%H:%M')
                    Representation(repr_date=test, repr_salle_places_restantes={}, event_id=event.id).save()
        return event
class UpdateDateEventForm(forms.Form):
    repr_date = forms.CharField(widget=forms.TextInput(attrs={'class':'SingleDate'}))

class ConfirmForm(forms.Form):
    CHOICES = [
        ('1', 'OUI'),
        ('2', 'NON'),
    ]
    choix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class ReservationForm(forms.ModelForm):
    class Meta: 
        model =  Reservation
        fields = [
        'reserv_email', 
        'reserv_nom',
        'reserv_prenom', 
        'reserv_tel'
        ]
        labels = {'reserv_email' : 'email', 'reserv_nom' : 'nom', 'reserv_prenom' : 'prenom', 'reserv_tel' : 'numéro de téléphone'}



        

