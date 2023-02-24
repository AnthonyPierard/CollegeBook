from django.urls import path
from . import views

app_name = 'college'
urlpatterns = [
    path('', views.visu_event, name='visu'),
    path('visu/<int:even_id>/', views.visu_detail, name='visu_detail'),
    path('creation_compte/', views.crea_compte),
    path('modif_compte/<int:admin_id>/', views.modif_compte),
    path('archiveruser/<int:admin_id>',views.archiver_compte, name='archiver_user'),
    path('afficher_admins/',views.admin_display),
    path('login/', views.login),
    path('newEvent/',views.cre_event)
]