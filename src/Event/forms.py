from datetime import datetime

from django import forms

from tagify.fields import TagField

from Event.models import Event, Representation, Price, CodePromo
from pathlib import Path
from Configuration.models import Config



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'image',
            'description',
            'duration',
            'user',
            'configuration',
            'artiste',

        ]
        labels = {'name': 'Nom de l\'événement', 'duration': 'Durée', 'description': 'Description', 'image': 'Illustration',
                  'user': 'Organisateurs', 'configuration' : 'Configuration', 'artiste' : 'Le(s) Artiste(s)'}

    date = forms.CharField(label='Date de l\'événement', widget=forms.TextInput(attrs={'class': 'MultiDate'}))

    drink_price = forms.FloatField(label='Prix des tickets boisson', min_value=0, widget=forms.NumberInput(attrs={"step":'0.01'}))

    food_price = forms.FloatField(label='Prix des tickets nourriture', min_value=0, widget=forms.NumberInput(attrs={"step":'0.01'}))

    promo_codes = TagField(label='Codes promo', delimiters=';', initial='FIRST : 3.00€;MAI : 5.00%')

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)

        if commit:
            event.save()

            #Representations creation in DB
            for user in self.cleaned_data["user"]:
                event.user.add(user)
            event = Event.objects.get(name=self.cleaned_data['name'])
            dates = self.cleaned_data['date'].split(', ')
            if dates != '':
                for date in dates:
                    date = datetime.strptime(date, '%d-%m-%Y/%H:%M')
                    Representation(date=date, remaining_seats={}, event_id=event.id).save()
                    #TODO remaining_seats


            codes_value = self.cleaned_data["promo_codes"]
            for element in codes_value:
                splitted = element.split(":")
                code_name = splitted[0].split(' ')[0].upper()
                code_amount = splitted[1].split(' ')[1]
                if "€" == code_amount[-1]:
                    CodePromo(code= code_name, amount= code_amount.replace("€", ""), event_id = event.id).save()
                elif "%" == code_amount[-1]:
                    CodePromo(code= code_name, percentage= code_amount.replace("%", ""), event_id = event.id).save()
            
            #Create 1 room per representation
            #TODO déplacer ça dans partie validation du brouillon
            event_name_json = self.cleaned_data["name"]
            event_config_name = self.cleaned_data["configuration"]
            event_config_url = Config.objects.get(name=event_config_name).url_json
            event_representations = Representation.objects.filter(event_id=event.id)
            path = Path(__file__).resolve().parent
            srcPath = path.parent
            src_file = srcPath.joinpath("Configuration" + event_config_url)
            if not path.joinpath("static/json/"+event_name_json).exists():
                path.joinpath("static/json/"+event_name_json).mkdir(parents=True,exist_ok=True)
            for represent in event_representations:
                dst_file = path /"static"/"json"/event_name_json/str(represent.id)
                dst_file = dst_file.with_suffix(".json")
                with open(src_file, "rb") as source_file:
                    with open(dst_file, "wb") as destination_file:
                        destination_file.write(source_file.read())



            # #Prices creation
            drink_price = float(self.cleaned_data["drink_price"])
            food_price = float(self.cleaned_data["food_price"])
            Price.objects.create(type="Boisson", price=drink_price, event_id=event.id).save()

            Price.objects.create(type="Nourriture", price=food_price, event_id=event.id).save()

        return event


class UpdateDateEventForm(forms.Form):
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'SingleDate'}))


class ConfirmForm(forms.Form):
    CHOICES = [
        ('1', 'OUI'),
        ('2', 'NON'),
    ]
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
