from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'sales'

urlpatterns = [
    path('transaction/update/<code>', views.transaction_update, name = 'transaction_update_status'),
    path('transaction/notification', views.transaction_notification, name = 'transaction_notification'),
]
