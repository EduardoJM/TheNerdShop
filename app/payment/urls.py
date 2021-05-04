from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('auth/', views.paymentAuth, name='payment_auth'),
]
