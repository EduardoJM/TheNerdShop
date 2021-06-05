

from .site import ShopAdminSite
from .products import ProductAdmin, CategoryAdmin
from .transactions import TransactionAdmin, TransactionItemAdmin
from ..models import Product, Category, Transaction, TransactionItem

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Transaction, TransactionAdmin)
admin_site.register(TransactionItem, TransactionItemAdmin)
