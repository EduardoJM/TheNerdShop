from django.db import models

from .product import Product, ProductSize

class Cart(models.Model):
    products = models.ManyToManyField(
        Product,
        through = 'CartProduct',
        through_fields = ('cart', 'product')
    )

    def add_to_cart(self, product, quantity, size = None):
        if size is None:
            size = product.get_default_size()
        cart_item = CartProduct.objects.filter(product = product, cart = self, size = size).first()
        # self.products.filter(pk = product.id).first()
        if cart_item is not None:
            # TODO: check quantity here
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.save()
            return
        cart_item = CartProduct()
        cart_item.cart = self
        cart_item.product = product
        cart_item.size = size
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
            size = ' - TAM ' + str(prod.size) if prod.size is not None else ''
            items['itemDescription' + str(ind)] = str(prod.product.name) + size
            items['itemAmount' + str(ind)] = "%.2f" % prod.product.real_price()
            items['itemQuantity' + str(ind)] = str(prod.quantity)
            ind = ind + 1
        return items

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete = models.CASCADE, null = True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)

    def total_price(self):
        return self.product.real_price() * self.quantity

    def product_size(self):
        if self.size is None:
            size = self.product.get_default_size()
            self.size = size
            self.save()
            return size
        return self.size

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
