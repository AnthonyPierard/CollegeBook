from django.contrib import admin

from .models import Evenement, Admin, Reservation, Salle, CodePromo

# Register your models here.

admin.site.register(Evenement)
admin.site.register(Admin)
admin.site.register(Reservation)
admin.site.register(Salle)
admin.site.register(CodePromo)