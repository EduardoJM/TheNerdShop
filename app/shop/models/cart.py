from django.db import models

from .product import Product

class Cart(models.Model):
    products = models.ManyToManyField(
        Product,
        through = 'CartProduct',
        through_fields = ('cart', 'product')
    )

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
