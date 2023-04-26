from django.urls import path
from .views import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .tasks import check_event_is_archived

app_name = 'Event'
urlpatterns = [
    path('', events_display, name='display'),
    path('details/<int:even_id>/', event_details, name='details'),
    path('creation/', event_creation, name='creation'),
    path('update_date/<int:representation_id>/', update_representation_date, name="update_date"),
    path('delete_representation/<int:representation_id>/', delete_representation, name="delete_representation"),
]

#peut etre meilleur endroit ou mettre ca  ?
scheduler = BackgroundScheduler()
scheduler.add_job(check_event_is_archived, CronTrigger.from_crontab('0 2 * * *'))  # Exécute tous les jours à 2:00 AM
scheduler.start()
