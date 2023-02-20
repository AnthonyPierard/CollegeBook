from django.urls import path
from . import views

app_name = 'college'
urlpatterns = [
    path('visu/', views.visu_event, name='visu'),
    path('visu/<int:even_id>/', views.visu_detail, name='visu_detail'),
    path('creation_compte/', views.crea_compte),
]