from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('auth/', views.paymentAuth, name='payment_auth'),
    path('script/', views.pagseguro_script, name = 'pagseguro_script'),
    path('finish/', views.payment_finish, name = 'payment_finish'),
]
