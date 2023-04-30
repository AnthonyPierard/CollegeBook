from datetime import datetime

from django.db import models

from Configuration.models import Place
from Event.models import Representation

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
    paid = models.BooleanField("État du payement", default=False)
    checkout_session = models.CharField("Session du payement", max_length=70, blank=True)

    # price = models.ForeignKey(Price, on_delete=models.CASCADE)

    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)

    def __str__(self):
        return "Reservation de " + self.last_name + " " + self.first_name + " pour le spectacle du " + str(self.representation.date)


class Ticket(PolymorphicModel):
    # drink_number = models.IntegerField("Ticket boisson pris avec la réservation", default=0)
    # food_number = models.IntegerField("Ticket nourriture pris avec la réservation", default=0)

    type = models.ForeignKey(Place, on_delete=models.CASCADE)

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class StandingTicket(Ticket):
    pass


class SeatingTicket(Ticket):
    seat_number = models.CharField("Trigramme du siège", max_length=3)
#
# class FoodTicket(Ticket):
#     seat_number = models.CharField("Trigramme du siège", max_length=3)
#
# class DrinkTicket(Ticket):
#     seat_number = models.CharField("Trigramme du siège", max_length=3)


