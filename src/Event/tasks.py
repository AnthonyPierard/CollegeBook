from datetime import datetime
from .models import Representation, Event
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def check_event_is_archived():
    print("TASK DONE")
    all_event_not_archived = Event.objects.filter(is_archived=False)
    for current in all_event_not_archived:
        if Representation.objects.filter(event=current.id, date__gte=datetime.now()).count() == 0:
            current.is_archived = True
            current.save()

scheduler = BackgroundScheduler()
scheduler.add_job(check_event_is_archived, CronTrigger.from_crontab('* * * * *'))  # Exécute tous les jours à 2:00 AM
scheduler.start()