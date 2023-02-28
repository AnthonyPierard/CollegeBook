from django.contrib import admin

from .models import User, Evenement, Reservation, Salle, CodePromo

# Register your models here.

admin.site.register(User)
admin.site.register(Evenement)
admin.site.register(Reservation)
admin.site.register(Salle)
admin.site.register(CodePromo)