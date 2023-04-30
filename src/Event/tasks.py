from .models import Representation, Event
from django.utils import timezone


def check_event_is_archived():
    print("TASK DONE")
    all_event_not_archived = Event.objects.filter(state='ACT')
    for current in all_event_not_archived:
        if Representation.objects.filter(event=current.id, date__gte=timezone.now()).count() == 0:
            current.state = 'ARC'
            current.save()


