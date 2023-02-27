from django.urls import path
from . import views

app_name = 'college'
urlpatterns = [
    path('', views.visu_event, name='visu'),
    path('visu/<int:even_id>/', views.visu_detail, name='visu_detail'),
    path('creation_compte/', views.crea_compte),
    path('modif_compte/<int:admin_id>/', views.modif_compte),
    # path('archiveruser/<int:admin_id>',views.archiver_compte, name='archiver_user'),
    path('afficher_admins/',views.admin_display, name='display_admin'),
    path('login/', views.admin_login),
    path('logout/', views.admin_logout),
    path('newEvent/',views.cre_event),
    path('change_super_admin/<int:admin_id>', views.admin_change_super),
    path('change_archived/<int:admin_id>', views.admin_change_archived),
    path('admin_event/<int:admin_id>/', views.admin_event, name="admin_event")
]