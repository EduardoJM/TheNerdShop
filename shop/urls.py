from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.AllProducts.as_view(), name='products'),
    path('products/category/<int:category_id>', views.CategoryProducts.as_view(), name='category'),
] + static('media/', document_root=settings.MEDIA_ROOT)
