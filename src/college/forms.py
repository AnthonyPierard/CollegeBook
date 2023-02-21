from django import forms
from django.core import validators
from .utils import check_password
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
        check_password(self)
    

class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_pseudo',
            'admin_superadmin',
            'admin_is_archived'
        ]
        labels = {'admin_pseudo': 'Pseudo','admin_superadmin':'Super Admin','admin_is_archived':'Compte archivé'}


