from shop.admin import admin_site

from .transactions import TransactionAdmin, TransactionItemAdmin
from ..models import Transaction, TransactionItem

admin_site.register(Transaction, TransactionAdmin)
admin_site.register(TransactionItem, TransactionItemAdmin)
