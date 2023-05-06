from django import forms
from django.forms import CharField, FloatField, IntegerField

from CollegeBook.utils import clean_tagify_string
from .models import Config, Place


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = [
            'name'
        ]
        labels = {'name': 'Nom de la nouvelle configuration'}

    classic_price = FloatField(label="Prix d'un siège classique", min_value=0.01, step_size=0.01, required=False)
    standing_price = FloatField(label="Prix des places debout", min_value=0.01, step_size=0.01, required=False)
    standing_number = IntegerField(label="Nombre de places debout", min_value=1, step_size=1, required=False)
    place_types = CharField(max_length=200, required=False)

    def save(self, user, commit=True):
        configuration = super(ConfigForm, self).save(commit=False)
        goodConfigName = configuration.name.replace(' ', '_')
        configuration.url_json = "/static/json/" + goodConfigName + ".json"
        configuration.user = user

        if commit:
            configuration.save()

            classic_price = self.cleaned_data["classic_price"]
            standing_price = self.cleaned_data["standing_price"]

            if classic_price:
                Place(type="Classique", price=classic_price, configuration_id=configuration.id).save()
            if standing_price:
                Place(type="Debout", price=standing_price, configuration_id=configuration.id).save()

            place_values = self.cleaned_data["place_types"]
            if place_values:
                cleaned_values = clean_tagify_string(place_values)
                for element in cleaned_values:
                    splitted = element.split(":")
                    if len(splitted) > 1:
                        place_type = splitted[0].split(' ')[0]
                        place_price = splitted[1].split(' ')[1].replace("€", "")

                        # Places creation in DB
                        Place(type=place_type, price=place_price, configuration_id=configuration.id).save()
