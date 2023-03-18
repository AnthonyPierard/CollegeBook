from django.db import models

from Account.models import User


class Config(models.Model):
    name = models.CharField('Nom de configuration', max_length=30, blank=True, unique=True)
    seating_arrangement = models.JSONField("Disposition de la salle", blank=True, null=True) #TODO retirer le blank ensuite mais pour teste ici

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.config_nom
