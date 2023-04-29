from django import forms
class ConfigForm(forms.Form):
    nom = forms.CharField()