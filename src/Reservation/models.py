from datetime import datetime

from django.db import models

from Event.models import Representation, Place, Price

from polymorphic.models import PolymorphicModel


class Reservation(models.Model):
    email = models.EmailField("Adresse mail de la reservation")
    last_name = models.CharField("Nom de la personne qui a réserver", max_length=50)
    first_name = models.CharField("Prénom de la personne qui réserve", max_length=50)
    phone = models.CharField("Numéro de tel de la personne qui réserve", max_length=10)
    date = models.DateTimeField("Date de la réservation", default=datetime.now())
    note = models.CharField("Remarque sur la réservation", max_length=1000)
    drink_number = models.IntegerField("Ticket boisson pris avec la réservation", default=0)
    food_number = models.IntegerField("Ticket nourriture pris avec la réservation", default=0)

    # price = models.ForeignKey(Price, on_delete=models.CASCADE)

    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)

    def __str__(self):
        return "Reservation n°" + str(self.number) + " pour le spectacle " + str(self.representation.date)


class Ticket(PolymorphicModel):
    # drink_number = models.IntegerField("Ticket boisson pris avec la réservation", default=0)
    # food_number = models.IntegerField("Ticket nourriture pris avec la réservation", default=0)

    type = models.ForeignKey(Place, on_delete=models.CASCADE)

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class StandingTicket(Ticket):
    pass


class SeatingTicket(Ticket):
    seat_number = models.CharField("Trigramme du siège", max_length=3)
