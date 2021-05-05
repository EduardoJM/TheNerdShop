#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User

from .site import ShopAdminSite
from .products import ProductAdmin, ProductImageAdmin, CategoryAdmin
from ..models import Product, ProductImage, Category

admin_site = ShopAdminSite(name='polls_admin')

#admin_site.register(User, UserAdmin)

admin_site.register(Product, ProductAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(Category, CategoryAdmin)
