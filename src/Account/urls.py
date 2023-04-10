from django.urls import path
from .views import *

app_name = 'Account'
urlpatterns = [
    path('signup', account_creation, name='creation'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('update/<int:user_id>/', update_account, name='update'),
    path('display', users_display, name='display'),
    path('update_admin/<int:user_id>/', user_update_admin, name='update_admin'),
    path('update_archive/<int:user_id>/', user_update_archive, name='update_archive'),
    path('events/<int:user_id>/', user_events_display, name="events"),

]