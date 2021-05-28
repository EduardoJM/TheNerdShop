

from .site import ShopAdminSite
from .products import ProductAdmin, ProductImageAdmin, CategoryAdmin
from .transactions import TransactionAdmin
from ..models import Product, ProductImage, Category, Transaction

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Transaction, TransactionAdmin)
