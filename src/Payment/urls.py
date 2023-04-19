from django.urls import path
from .views import *

app_name = 'Payment'
urlpatterns = [
    path('cancel/', cancel , name='cancel'),
    path('success/', success , name='success'),
    path('checkout/<pk>', CreateCheckoutSessionView.as_view() , name='CreateCheckoutSessionView'),
    path('', ProductLandingPageView , name='landing'),
]