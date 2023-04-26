from datetime import datetime
from .models import Representation, Event



def check_event_is_archived():
    all_event_not_archived = Event.objects.filter(is_archived=False)
    for current in all_event_not_archived:
        if Representation.objects.filter(event=current.id, date__gte=datetime.now()).count() == 0:
            current.is_archived = True
            current.save()
