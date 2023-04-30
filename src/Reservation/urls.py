from django.urls import path
from .views import *

app_name = 'Reservation'
urlpatterns = [
    path('seat_selection/<int:representation_id>/', seat_selection, name="seat_selection"),
    path('representation_reservation/<int:representation_id>/', representation_reservation, name="representation_reservation"),
    path('seat_selection/<int:representation_id>/process_price/', process_price, name="process_price"),
]
