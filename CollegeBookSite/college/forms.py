from django import forms
from django.core import validators

from .models import Admin

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_pseudo',
            'admin_password',
            'admin_superadmin',
        ]
        labels = {'admin_pseudo': 'Pseudo', 'admin_password':'Password','admin_superadmin':'Super Admin'}
        widgets = {'admin_password': forms.PasswordInput}
    # pseudo = forms.CharField(label='Pseudonyme',max_length=50, required = True)
    # password = forms.CharField(label='Password', max_length=50, required = True, widget = forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=50, required = True, widget = forms.PasswordInput)
    # is_super = forms.BooleanField(label='Super Admin', required=False)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            # (À définir) Choisir la forme d'erreur entre ces deux options : 
            # - self.add_error('confirm_password', 'La confirmation du mot de passe n\'est pas correcte')
            # - raise forms.ValidationError('La confirmation du mot de passe n\'est pas correcte')
            pass

    

