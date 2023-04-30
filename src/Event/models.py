from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from Account.models import User
from Configuration.models import Config
from CollegeBook.settings import TIME_ZONE
from zoneinfo import ZoneInfo
import pytz


class Event(models.Model):
    STATES =[
        ("DRF", "Draft"),
        ("ACT", "Active"),
        ("ARC", "Archived")
    ]
    name = models.CharField("Nom de l'événement", max_length=200, unique=True)
    description = models.CharField("Description de l'événement", max_length=1000)
    image = models.ImageField("Image(s) de l'événement(s)", upload_to="Images/", blank=True, null=True)
    duration = models.TimeField("Durée de l'événement", default='02:00')
    state = models.CharField("Etat de l'event brouillon/actif/archivé", choices=STATES, max_length=3, default="DRF")
    artiste = models.CharField("Artistes", max_length= 2000)

    configuration = models.ForeignKey(Config, on_delete=models.CASCADE)

    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class CodePromo(models.Model):
    code = models.CharField("Le code à introduire", max_length=20)
    amount = models.FloatField("Montant fixe de réduction", blank=True, default=0)
    percentage = models.FloatField("Pourcentage de reduction sur le prix total", blank=True, default=0)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{}___{}".format(self.code, self.event.name)


class Representation(models.Model):
    date = models.DateTimeField("Date", default=datetime.now())
    remaining_seats = models.JSONField("Informations de la salle", blank=True, null=True)  # TODO pour tester aussi il faudra retirer blank et null

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name + " le " + str(datetime.makenaive(self.date).strftime('%d/%m/%Y à %H:%M'))


@receiver(pre_save, sender=Representation)
def trigger_representation_at_same_time(sender, instance, *args, **kwargs):
    all_rep_same_day = Representation.objects.filter(date__day=instance.date.day).exclude(pk=instance.id)   #on recupere toutes les representations du meme jour sauf lui meme en cas de modif
    event_instance = Event.objects.get(pk=instance.event.id)
    if event_instance is None:
        pass
    instance_duration = event_instance.duration                                                             #recupere la duree de la rep qu'on essaye d ajouter
    i_date = datetime.combine(instance.date, instance.date.time()).astimezone(pytz.utc)                     #on transforme la date en UTC+0
    instance_datetime_date = datetime(year=i_date.year,                                                     #on garde la date UTC+0 MAIS on lui rajoute le +2000 apres
                                      month=i_date.month,
                                      day=i_date.day,
                                      hour=i_date.hour,
                                      minute=i_date.minute,
                                      second=i_date.second,
                                      tzinfo=ZoneInfo(TIME_ZONE))
    instance_time_end = instance_datetime_date + timedelta(hours=instance_duration.hour,                    #on cree l heure de fin pour les tests
                                                           minutes=instance_duration.minute,
                                                           seconds=instance_duration.second)
    for rep in all_rep_same_day:                                                                            #on boucle sur toutes les rep
        rep_datetime_date = datetime.combine(rep.date, rep.date.time(), tzinfo=ZoneInfo(TIME_ZONE))         #on met la date de rep au meme format que celle de instance
        rep_duration = Event.objects.get(pk=rep.event.id).duration                                          #on recupere sa duree
        rep_time_end = rep_datetime_date + timedelta(hours=rep_duration.hour, minutes=rep_duration.minute,  #on cree la date de fin de rep pour les tests
                                                     seconds=rep_duration.second)

        if rep_datetime_date <= instance_datetime_date <= rep_time_end:
            event_instance.delete()
            raise ValueError("Une représentation à déjà lieu à ce moment là")
        if rep_datetime_date <= instance_time_end <= rep_time_end:
            event_instance.delete()
            raise ValueError("Une représentation à déjà lieu à ce moment là")
        if instance_datetime_date <= rep_datetime_date and instance_time_end >= rep_time_end:
            event_instance.delete()
            raise ValueError("Une représentation à déjà lieu à ce moment là")



# TODO faire un trigger pour qu'un event soit supp si plus AUCUNE reprensentation existante


class Price(models.Model):
    type = models.CharField("Nom de l'élément", max_length=50)
    price = models.DecimalField("Prix de l'élément'", max_digits=3, decimal_places=2)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
