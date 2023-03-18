from django.urls import path
from .views import *

app_name = 'Configuration'
urlpatterns = [
    path('reservation/<int:representation_id>/', reservation, name="reservation"),
]
