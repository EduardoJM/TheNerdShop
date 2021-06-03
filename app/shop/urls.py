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
    path('cart/', views.cart, name = 'user_cart'),
    path('cart/user/update', views.cart_update_user, name = 'user_cart_update'),
    path('cart/confirm', views.cart_confirm, name = 'user_cart_confirm'),
    path('cart/payment', views.cart_payment, name = 'user_cart_payment'),
    path('cart/add', views.add_to_cart, name = 'add_to_cart'),
    path('cart/remove/<int:register_id>', views.remove_from_cart, name = 'remove_from_cart'),
    path('sign-up/', views.sign_up, name = 'sign_up'),
    path('sign-in/', views.sign_in, name = 'sign_in'),
    path('sign-out/', views.sign_out, name = 'sign_out'),
    path('transaction/update/<code>', views.transaction_update, name = 'transaction_update_status'),
    path('transaction/notification', views.transaction_notification, name = 'transaction_notification'),
] + static('media/', document_root=settings.MEDIA_ROOT)
