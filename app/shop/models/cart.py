from django.db import models

from .product import Product

class Cart(models.Model):
    products = models.ManyToManyField(
        Product,
        through = 'CartProduct',
        through_fields = ('cart', 'product')
    )

    def add_to_cart(self, product, quantity):
        cart_item = self.products.filter(pk = product.id).first()
        if cart_item is not None:
            # TODO: check quantity here
            cart_item.quantity = cart_item.quantity + quantity
            return
        cart_item = CartProduct()
        cart_item.cart = self
        cart_item.product = product
        ## TODO: check quantity here
        cart_item.quantity = quantity
        cart_item.save()
        return
    
    def get_cart_items(self):
        return CartProduct.objects.filter(cart = self.pk)

    def total_itens(self):
        products = self.get_cart_items()
        total = 0
        for prod in products:
            total += prod.quantity
        return total

    def total_price(self):
        products = self.get_cart_items()
        total = 0
        for prod in products:
            total += prod.total_price()
        return total

    def serialize_cart(self):
        products = self.get_cart_items()
        items = {}
        ind = 1
        for prod in products:
            items['itemId' + str(ind)] = str(prod.product.id)
            items['itemDescription' + str(ind)] = str(prod.product.name)
            items['itemAmount' + str(ind)] = "%.2f" % prod.product.real_price()
            items['itemQuantity' + str(ind)] = str(prod.quantity)
            ind = ind + 1
        return items

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)

    def total_price(self):
        return self.product.real_price() * self.quantity

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
