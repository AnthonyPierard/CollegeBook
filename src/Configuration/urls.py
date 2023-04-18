from django.urls import path
from .views import *

app_name = 'Config'
urlpatterns = [
    path('', area_configuration, name="Configuration"),
    path('create_json/', create_json, name="create_json"),
]
