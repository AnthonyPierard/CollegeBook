from datetime import datetime

from django.db import models
from Account.models import User
from Configuration.models import Config


class Event(models.Model):
    name = models.CharField("Nom de l'événement", max_length=200, unique=True)
    description = models.CharField("Description de l'événement", max_length=1000)
    image = models.ImageField("Image(s) de l'événement(s)", upload_to="Images/", blank=True, null=True)
    duration = models.TimeField("Durée de l'événement", default='02:00')
    artiste = models.CharField("Artistes", max_length= 2000)

    configuration = models.ForeignKey(Config, on_delete=models.CASCADE)  # todo Retirer le null=True

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
    remaining_places = models.JSONField("Informations de la salle", blank=True, null=True)  # TODO pour tester aussi il faudra retirer blank et null

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name + " " + str(self.date.strftime('%d/%m/%Y'))

#TODO faire un trigger pour qu'un event soit supp si plus AUCUNE reprensentation existante


class Place(models.Model):
    type = models.CharField("Nom de la place", max_length=50)
    price = models.DecimalField("Prix de la place", max_digits=5, decimal_places=2)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Price(models.Model):
    type = models.CharField("Nom de l'élément", max_length=50)
    price = models.DecimalField("Prix de l'élément'", max_digits=3, decimal_places=2)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
