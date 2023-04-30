from django.urls import path
from .views import *

app_name = 'Validation'
urlpatterns = [
    # path('cancel/', cancel , name='cancel'),
    path('scan_ticket/<str:code>/', scan_ticket, name='scan_ticket'),
    path('validated_ticket/<str:code>/', validation_ticket, name='validation')
]
