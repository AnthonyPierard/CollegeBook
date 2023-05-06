from django import forms
from tagify.fields import TagField
from .models import Config, Place
class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = [
            'name'
        ]
        labels = {'name': 'Nom de la nouvelle configuration'}

    place_types = TagField(label='Types de places', delimiters=';',
                           initial='Debout : 3.00€;Classic : 4.00€;Vip : 5.00€')


    def save(self, user, commit=True):
        configuration = super(ConfigForm, self).save(commit=False)
        goodConfigName = configuration.name.replace(' ', '_')
        configuration.url_json = "/static/json/" + goodConfigName + ".json"
        configuration.user = user

        if commit:
            configuration.save()
            #TODO Afficher les bon types de places dans le tagify pour chaque configuration proposée dans area_configuration
            place_values = self.cleaned_data["place_types"]
            for element in place_values:
                splitted = element.split(":")
                if(len(splitted)>1):
                    place_type = splitted[0].split(' ')[0]
                    place_price = splitted[1].split(' ')[1].replace("€", "")

                    # Places creation in DB
                    Place(type=place_type, price=place_price, configuration_id=configuration.id).save()
