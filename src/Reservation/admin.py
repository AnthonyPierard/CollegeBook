from django.contrib import admin

from .models import Ticket, Place, Representation, Reservation
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Place)
admin.site.register(Representation)
admin.site.register(Reservation)