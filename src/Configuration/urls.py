from django.urls import path
from .views import *

app_name = 'Config'
urlpatterns = [
    path('', area_configuration, name="Configuration"),
    path('create_json/', create_json, name="create_json"),
    path('get_place_types/<str:config_name>/', get_place_types, name="get_place_types"),
]
