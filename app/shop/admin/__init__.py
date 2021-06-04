

from .site import ShopAdminSite
from .products import ProductAdmin, CategoryAdmin
from .transactions import TransactionAdmin
from ..models import Product, Category, Transaction

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Transaction, TransactionAdmin)
