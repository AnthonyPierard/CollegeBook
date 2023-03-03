from django import forms
from django.core import validators
from .utils import check_password
from .models import Evenement, User

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
            'even_date',
            'even_duree',
            #'event_time',
            'configuration_salle',
            'admin'

            #'can_moderate',
            #'promo_code'

            
        ]
        lables = {'event_nom' : 'Nom','even_date':'date','even_duree':'Durée','even_description': 'desc', 'even_illustration':'illus','configuration_salle':'conf', 'admin':'Organisateurs'}

    # def save(self, request, commit=True):
    #     event = super(EventForm, self).save(commit=False)
    #     event.admin_id = request.user.id
    #     if commit:
    #         event.save()
    #     return event
class UpdateDateEventForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = [
            'even_date',
        ]
        lables = {'even_date' : ''}