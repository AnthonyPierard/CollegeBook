from django.urls import path
from .views import *

app_name = 'Event'
urlpatterns = [
    path('', events_display, name='display'),
    path('details/<int:even_id>/', event_details, name='details'),
    path('creation/', event_creation, name='creation'),
    path('update_date/<int:representation_id>/', update_representation_date, name="update_date"),
    path('delete_representation/<int:representation_id>/', delete_representation, name="delete_representation"),
    path('update_event/<int:event_id>/', event_update, name='update'),
    path('publish_event/<int:event_id>/', publish_event, name='publish_event'),
    path('delete_event_draft/<int:event_id>/', delete_event_draft, name='delete_draft')
]

