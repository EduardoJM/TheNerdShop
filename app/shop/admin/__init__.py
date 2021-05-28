

from .site import ShopAdminSite
from .products import ProductAdmin, ProductImageAdmin, CategoryAdmin
from ..models import Product, ProductImage, Category

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(Category, CategoryAdmin)

