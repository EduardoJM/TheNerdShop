from django.db import models
from django.utils.html import format_html
from datetime import datetime
import markdown

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

    def render_description(self):
        return format_html(markdown.markdown(self.description))

    def real_price(self):
        if self.discount_price > 0:
            return self.discount_price
        return self.price

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'