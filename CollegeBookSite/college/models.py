from django.db import models
from datetime import datetime

# Create your models here.

class Evenement(models.Model):
    #les id sont automatiquement créer par django
    even_nom = models.CharField("Nom de l'évènement",max_length=200, unique=True)
    even_date = models.DateTimeField("Date de l'évènement")
    even_description = models.CharField("Description de l'évènement", max_length=1000)
    even_illustration = models.ImageField("Image(s) de l'évènement(s)",upload_to="url mis dans MEDIA_ROOT dans settings", blank=True)

    def __str__(self):
        return self.even_nom
    
class Reservation(models.Model):
    
    reserv_email = models.EmailField("Adresse mail de la reservation")
    reserv_nom = models.CharField("Nom de la personne qui a réserver", max_length=50)
    reserv_prenom = models.CharField("Prénom de la personne qui réserve", max_length=50)
    reserv_tel = models.CharField("Numéro de tel de la personne qui réserve", max_length=10)
    reserv_date = models.DateTimeField("Date de la réservation", default=datetime.now())
    reserv_remarque = models.CharField("Remarque sur la réservation", max_length=1000)
    reserv_numero = models.IntegerField("Numéro du ticket pour le spectatcle")
    #si il y a besoin de plus d'info : type de boisson, nombre de boisson, ...
    #alors on devrait créer une nouvelle table pour les boissons et la nourriture
    reserv_boisson = models.BooleanField("Ticket boisson pris avec la réservation")
    reserv_nourriture = models.BooleanField("Ticket nourriture pris avec la réservation")
    
    #a mon avis plus de chose a faire pour la clé secondaire ()
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    def __str__(self):
        return "Ticket n°" + str(self.reserv_numero) + " pour le spectacle " + self.evenement
