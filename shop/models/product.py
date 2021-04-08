from django.db import models
from datetime import datetime

from .productImage import ProductImage
from .category import Category

class Product(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    images = models.ManyToManyField(ProductImage)
    categories = models.ManyToManyField(Category)
    created_date = models.DateTimeField('Data', default=datetime.now, blank=True)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)
    discount_price = models.DecimalField('Preço com Desconto', decimal_places=2, max_digits=8)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'