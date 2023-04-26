from django.urls import path
from .views import *

app_name = 'Payment'
urlpatterns = [
    path('cancel/', cancel , name='cancel'),
    path('success/', success , name='success'),
    path('checkout/<int:representation_id>', CreateCheckoutSessionView.as_view() , name='CreateCheckoutSessionView'),
    path('landing/<int:representation_id>', landing , name='landing'),
]