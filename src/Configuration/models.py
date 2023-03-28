from django.db import models

from Account.models import User


class Config(models.Model):
    name = models.CharField('Nom de configuration', max_length=30, blank=True, unique=True)
    seating_arrangement = models.JSONField("Disposition de la salle", blank=True, null=True) #TODO retirer le blank ensuite mais pour teste ici
    url_json = models.CharField('URL du fichier json', max_length=100, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
