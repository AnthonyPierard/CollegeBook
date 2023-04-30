from django.urls import path
from .views import *

app_name = 'Event'
urlpatterns = [
    path('', events_display, name='display'),
    path('details/<int:even_id>/', event_details, name='details'),
    path('creation/', event_creation, name='creation'),
    path('update_date/<int:representation_id>/', update_representation_date, name="update_date"),
    path('delete_representation/<int:representation_id>/', delete_representation, name="delete_representation"),
]

