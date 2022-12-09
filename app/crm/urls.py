from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from shop.admin import admin_site

from . import views

app_name = 'crm'
urlpatterns = [
    path('', admin_site.admin_view(views.index), name='index'),
]
