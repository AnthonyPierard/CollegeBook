from Event.models import Representation
from django.utils import timezone
from django.shortcuts import redirect



def stripe_id_creation(place_type, event_name):
    stripe_id = place_type.lower() + ''.join([element.capitalize() for element in event_name.split(' ')])
    return stripe_id

def check_if_representation_is_passed(representation_id,redirect_url,*args):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        print("OK")
        return redirect(redirect_url, *args)
