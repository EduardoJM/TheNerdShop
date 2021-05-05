from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.AllProducts.as_view(), name='products'),
    path('products/category/<int:category_id>', views.CategoryProducts.as_view(), name='category'),
    path('products/detail/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('sign-up', views.sign_up, name = 'sign_up'),
    path('sign-in', views.sign_in, name = 'sign_in'),
    path('sign-out', views.sign_out, name = 'sign_out'),
] + static('media/', document_root=settings.MEDIA_ROOT)
