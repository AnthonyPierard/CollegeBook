"""CollegeBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Event.tasks import check_event_is_archived, send_remainders_mail, send_thanks_mail

from . import settings

urlpatterns = [
    path('', include("Event.urls")),
    path('admin/', admin.site.urls),
    path('account/', include("Account.urls")),
    path('configuration/', include("Configuration.urls")),
    path('reservation/', include("Reservation.urls")),
    path('payment/', include("Payment.urls")),
    path('validation/', include('Validation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print("setup tasks")
scheduler = BackgroundScheduler()
scheduler.add_job(check_event_is_archived, CronTrigger.from_crontab('* * * * *'))  # Exécute toutes les minutes
scheduler.add_job(send_remainders_mail, CronTrigger.from_crontab('0 2 * * *'))  # Exécute toutes les minutes
scheduler.add_job(send_thanks_mail, CronTrigger.from_crontab('0 2 * * *'))  # Exécute toutes les minutes
scheduler.start()