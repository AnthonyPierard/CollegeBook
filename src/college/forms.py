from django import forms
from django.core import validators
from .utils import check_password
from .models import Admin,Evenement

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_prenom',
            'admin_nom',
            'admin_email',
            'admin_password',
            'admin_superadmin',
        ]
        labels = {'admin_prenom': 'Prenom','admin_nom':'Nom','admin_email':'Email', 'admin_password':'Password','admin_superadmin':'Super Admin'}
        widgets = {'admin_password': forms.PasswordInput}
    # pseudo = forms.CharField(label='Pseudonyme',max_length=50, required = True)
    # password = forms.CharField(label='Password', max_length=50, required = True, widget = forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=50, required = True, widget = forms.PasswordInput)
    # is_super = forms.BooleanField(label='Super Admin', required=False)
    def clean_confirm_password(self):
        check_password(self)
    

class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_prenom',
            'admin_nom',
            'admin_email',

        ]
        labels = {'admin_prenom': 'Prenom','admin_nom':'Nom','admin_email':'Email'}

class LoginAdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_email',
            'admin_password',         
        ]
        labels = {'admin_email': 'Email', 'admin_password':'Password'}
        widgets = {'admin_password': forms.PasswordInput}

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
            'configuration_salle'

            #'can_moderate',
            #'promo_code'

            
        ]
        lables = {'event_nom' : 'Nom','even_date':'date','even_duree':'Durée','even_description': 'desc', 'even_illustration':'illus','configuration_salle':'conf'}

