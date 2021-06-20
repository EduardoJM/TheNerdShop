from .site import ShopAdminSite
from .products import ProductAdmin, CategoryAdmin
from .user import UserAdmin
from ..models import Product, Category, User

admin_site = ShopAdminSite(name='shop_admin')

admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(User, UserAdmin)
