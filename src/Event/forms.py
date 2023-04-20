from datetime import datetime

from django import forms

from tagify.fields import TagField

from Event.models import Event, Representation

from CollegeBook.utils import stripe_id_creation

import stripe

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'image',
            'description',
            'duration',
            'user'

        ]
        labels = {'name': 'Nom de l\'événement', 'duration': 'Durée', 'description': 'desc', 'image': 'Illustration',
                  'user': 'Organisateurs'}

    date = forms.CharField(label='Date de l\'événement', widget=forms.TextInput(attrs={'class': 'MultiDate'}))

    place_types = TagField(label='Types de places', delimiters=';', initial='Classic : 3.00€;Golang : 5.00€')

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)

        if commit:
            event.save()
            for user in self.cleaned_data["user"]:
                event.user.add(user)
            dates = self.cleaned_data['date'].split(', ')
            if dates != '':
                event = Event.objects.get(name=self.cleaned_data['name'])
                for date in dates:
                    test = datetime.strptime(date, '%d-%m-%Y/%H:%M')
                    Representation(date=test, remaining_places={}, event_id=event.id).save()



            #Create a stripe product
            place_values = self.cleaned_data["place_types"]
            event_name = self.cleaned_data["name"]
            for element in place_values:
                splitted = element.split(":")
                place_type = splitted[0].split(' ')[0]
                place_price = splitted[1].split(' ')[1].replace("€","")

                stripe.Product.create(
                    name= "Siège " + place_type.capitalize() + " [" + event_name + "]",
                    default_price_data= {
                        'unit_amount': int(float(place_price) * 100),
                        'currency': 'eur'
                    },
                    id= stripe_id_creation(place_type, event_name)
                )
        return event


class UpdateDateEventForm(forms.Form):
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'SingleDate'}))


class ConfirmForm(forms.Form):
    CHOICES = [
        ('1', 'OUI'),
        ('2', 'NON'),
    ]
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
