from django.db import models
from datetime import datetime,timedelta
from datetime import date
from django.db.models.signals import(pre_save)
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
# from django.contrib.auth.models import User
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(('Adresse email'), unique=True)
    first_name = models.CharField(('Prénom'), max_length=30, blank=True)
    last_name = models.CharField(('Nom de famille'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('Date de création'), auto_now_add=True)
    last_login = models.DateTimeField(('Dernier login'), auto_now_add=True, null=True)
    is_active = models.BooleanField(('Actif'), default=True)
    is_staff = models.BooleanField(('SuperAdmin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def __str__(self) -> str:
        """
        Show the email when printed
        """
        return self.email

    def super_admin_update(self):
        self.is_staff = not self.is_staff
        self.is_superuser = not self.is_superuser

    def archive_admin(self):
        self.is_active = not self.is_active
   
# @receiver(pre_save,sender=Admin)
# def trigger_not_same_email(sender,instance,*args,**kwargs):
#     others_admins = Admin.objects.filter(admin_email = instance.admin_email)
#     if others_admins.count() > 0 :
#         raise ValueError("Email déjà attribuée à un autre admin")


class Salle(models.Model):

    salle_nom = models.CharField("Nom de la salle",max_length=50)
    salle_nbr_places_normal = models.IntegerField("Nombres de places normales")
    salle_configuration = models.FileField("Sauvegarde de la configuration de la salle")#definir le type de fichier que l'on veut pour les configurations (.json  ?) - emile

    createur = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.salle_nom

@receiver(pre_save,sender=Salle)
def trigger_not_same_salle(sender,instance,*args,**kwargs):
    others_salles = Salle.objects.filtre(salle_nom = instance.salle_nom).filtre(createur = instance.createur)
    if others_salles.count() > 0:
        raise ValueError("Ce nom de configuration de salle existe deja")

class Evenement(models.Model):
    #les id sont automatiquement créer par django
    even_nom = models.CharField("Nom de l'événement",max_length=200, unique=True)
    even_date = models.DateTimeField("Date",default=datetime.now())
    even_description = models.CharField("Description de l'évènement", max_length=1000)
    even_illustration = models.ImageField("Image(s) de l'évènement(s)",upload_to="Images/", blank=True, null=True)
    #event_time = models.TimeField("Heure",default=datetime.now)
    configuration_salle = models.CharField("Configuration de la salle",choices=[("1","classique"),("2","espacée"),("3","proche")],max_length=2000,default="classique")# ici faut faire une foreignKey avec les Salles pour le choices. Je change pas encore pour pas casser la vue - emile
    #can_moderate = trouver comment faire l'espèce de double liste de la maquette
    #promo_code
    even_duree = models.TimeField("Durée de l'événement",default='02:00')
    admin = models.ManyToManyField(User)
    #pour tester un simple evenement je le met en commentaire
    #configuration = models.ForeignKey(Salle,on_delete=models.CASCADE)

    def __str__(self):
        return self.even_nom

@receiver(pre_save,sender=Evenement)
def trigger_not_events_same_time(sender,instance,*args,**kwargs):
    others_events = Evenement.objects.filter(even_date__date=instance.even_date.date())
    for event in others_events:
        # print(datetime.combine(event.even_date, event.even_duree))
        # print(instance.even_date)$
        print(event.even_date.hour)
        print(event.even_date.minute)
        if event.even_date + timedelta(hours=event.even_duree.hour, minutes= event.even_duree.minute) >= instance.even_date \
            and instance.even_date + timedelta(hours=instance.even_duree.hour,minutes=instance.even_duree.minute) >= event.even_date:
            raise ValueError("Un event est déja prévu sur ce créneau horaire")


class Reservation(models.Model):
    
    reserv_email = models.EmailField("Adresse mail de la reservation")
    reserv_nom = models.CharField("Nom de la personne qui a réserver", max_length=50)
    reserv_prenom = models.CharField("Prénom de la personne qui réserve", max_length=50)
    reserv_tel = models.CharField("Numéro de tel de la personne qui réserve", max_length=10)
    reserv_date = models.DateTimeField("Date de la réservation", default=datetime.now())
    reserv_remarque = models.CharField("Remarque sur la réservation", max_length=1000)
    reserv_numero = models.IntegerField("Numéro du ticket pour le spectatcle")
   
    
    #a mon avis plus de chose a faire pour la clé secondaire ()
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    def __str__(self):
        return "Ticket n°" + str(self.reserv_numero) + " pour le spectacle " + self.evenement

class CodePromo(models.Model):

    codepromo_code = models.CharField("Le code à introduire",max_length=20)
    codepromo_montant = models.FloatField("Montant fixe de réduction",blank=True,default=0)
    codepromo_pourcentage = models.FloatField("Pourcentage de reduction sur le prix total",blank=True,default=0)#faut faire des triggers, jsp comment faire - emile

    Evenement = models.ForeignKey(Evenement,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}___{}".format(self.codepromo_code , self.Evenement.even_nom)

@receiver(pre_save,sender = CodePromo)
def trigger_not_same_codepromo(sender,instance,*args,**kwargs):
    others_codepromo = sender.objects.filter(codepromo_code=instance.codepromo_code).filter(Evenement=instance.Evenement)
    if others_codepromo.count() > 0:
        raise ValueError("Ce code existe déjà pour cet événement")

class Ticket(models.Model):
    ticket_siege = models.CharField("Trigramme du siège",max_length=3)
    ticket_debout = models.BooleanField("Place debout ou assise",default=False)
    ticket_prix = models.FloatField("Prix de la place")
    #si il y a besoin de plus d'info : type de boisson, nombre de boisson, ...
    #alors on devrait créer une nouvelle table pour les boissons et la nourriture
    ticket_boisson = models.IntegerField("Ticket boisson pris avec la réservation",default=0) # je metterai des Integer ici pour le nombre de tickets boissons et nourriture achetés - emile
    ticket_nourriture = models.IntegerField("Ticket nourriture pris avec la réservation",default=0) # same
    Reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE)

# !!! bien faire une migration de la db à chaque fois qu'elle est modifiée !!!
# executer les commandes :
# py manage.py makemigrations college
# py manage.py migrate


    
