from django import forms

from .models import User
from CollegeBook.utils import check_password


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff',
        ]
        labels = {'first_name': 'Prénom', 'last_name': 'Nom', 'email': 'Email', 'password': 'Mot de passe',
                  'is_staff': 'Super Admin'}
        widgets = {'password': forms.PasswordInput}

    confirm_password = forms.CharField(label='Confirmer le mot de passe', max_length=50, required=True,
                                       widget=forms.PasswordInput)

    def clean_confirm_password(self):
        check_password(self)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginUserForm(forms.Form):
    email = forms.CharField(label='Email', max_length=50, required=True)
    password = forms.CharField(label='Mot de passe', max_length=50, required=True, widget=forms.PasswordInput)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        labels = {'first_name': 'Prénom', 'last_name': 'Nom', 'email': 'Email'}
