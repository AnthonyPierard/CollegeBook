from datetime import datetime

from django import forms

from Event.models import Event, Representation


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
        lables = {'name': 'Nom de l\' événement', 'duration': 'Durée', 'description': 'desc', 'image': 'Illustration',
                  'user': 'Organisateurs'}

    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'MultiDate'}))

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
        return event


class UpdateDateEventForm(forms.Form):
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'SingleDate'}))


class ConfirmForm(forms.Form):
    CHOICES = [
        ('1', 'OUI'),
        ('2', 'NON'),
    ]
    choix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
