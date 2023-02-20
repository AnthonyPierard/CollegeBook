from django.db import models
from datetime import datetime

# Create your models here.

class Admin(models.Model):

    admin_pseudo = models.CharField("Pseudo de l admin",max_length=50)
    admin_password = models.CharField("Mot de passe de l admin",max_length=100)
    admin_superadmin = models.BooleanField("Est un super admin ou non",default=False)

    def __str__(self) -> str:
        return self.admin_pseudo

class Salle(models.Model):

    salle_nom = models.CharField("Nom de la salle",max_length=50)
    salle_nbr_places_normal = models.IntegerField("Nombres de places normales")
    salle_configuration = models.FileField("Sauvegarde de la configuration de la salle")#definir le type de fichier que l'on veut pour les configurations (.json  ?) - emile


    createur = models.ForeignKey(Admin,on_delete=models.CASCADE)

class Evenement(models.Model):
    #les id sont automatiquement créer par django
    even_nom = models.CharField("Nom de l'évènement",max_length=200, unique=True)
    even_date = models.DateTimeField("Date de l'évènement")
    even_description = models.CharField("Description de l'évènement", max_length=1000)
    even_illustration = models.ImageField("Image(s) de l'évènement(s)",upload_to="Images", blank=True, null=True)

    admin = models.ForeignKey(Admin,on_delete=models.CASCADE, null= True)
    #pour tester un simple evenement je le met en commentaire
    #configuration = models.ForeignKey(Salle,on_delete=models.CASCADE)

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
    reserv_boisson = models.IntegerField("Ticket boisson pris avec la réservation") # je metterai des Integer ici pour le nombre de tickets boissons et nourriture achetés - emile
    reserv_nourriture = models.IntegerField("Ticket nourriture pris avec la réservation") # same
    
    #a mon avis plus de chose a faire pour la clé secondaire ()
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    def __str__(self):
        return "Ticket n°" + str(self.reserv_numero) + " pour le spectacle " + self.evenement

class CodePromo(models.Model):

    codepromo_code = models.CharField("Le code à introduire",max_length=20)
    codepromo_montant = models.FloatField("Montant fixe de réduction",blank=True)
    codepromo_pourcentage = models.FloatField("Pourcentage de reduction sur le prix total",blank=True)#faut faire des triggers, jsp comment faire - emile

    Evenement = models.ForeignKey(Evenement,on_delete=models.CASCADE)


# !!! bien faire une migration de la db à chaque fois qu'elle est modifiée !!!
# executer les commandes :
# py manage.py makemigrations college
# py manage.py migrate


    