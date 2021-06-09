from .site import ShopAdminSite
from .products import ProductAdmin, CategoryAdmin
from ..models import Product, Category

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
