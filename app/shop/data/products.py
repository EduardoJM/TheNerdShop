from django.db.models import Q

from ..models import Product
from sales.models import TransactionItem

def get_purchase_quantity_price(product):
    items = TransactionItem.objects.filter(
        product = product,
    ).filter(
        Q(transaction__transaction_status = 3) | Q(transaction__transaction_status = 4),
    )
    quantity = 0
    total_price = 0
    for item in items:
        quantity += item.quantity
        total_price += float(item.total_price())
    return quantity, total_price

def get_products_purchase_quantity_price():
    products = Product.objects.all()
    data = []
    for product in products:
        quantity, total_price = get_purchase_quantity_price(product)
        data += [
            {
                'product': product.name,
                'quantity': quantity,
                'total_price': round(total_price, 2),
            }
        ]
    data.sort(key = lambda x : x['total_price'], reverse = True)
    accumulated = 0
    for i in range(0, len(data)):
        accumulated += data[i]['total_price']
        data[i]['accumulated_price'] = round(accumulated, 2)
    for i in range(0, len(data)):
        data[i]['accumulated_percent'] = round(0 if accumulated == 0 else data[i]['accumulated_price'] / accumulated, 2)
    return data
