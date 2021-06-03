from django.db import models
from django.utils.html import format_html
from datetime import datetime
import markdown

from .category import Category

class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/products')

    def __str__(self):
        return self.alternative_text

    class Meta:
        verbose_name = 'Imagens de Produtos'
        verbose_name_plural = 'Imagens de Produtos'

class Product(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    images = models.ManyToManyField(ProductImage)
    categories = models.ManyToManyField(Category)
    created_date = models.DateTimeField('Data', default=datetime.now, blank=True)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)
    discount_price = models.DecimalField('Preço com Desconto', decimal_places=2, max_digits=8)

    def has_various_sizes(self):
        return len(self.get_sizes()) > 1

    def get_sizes(self):
        if len(self.productsize_set.all()) == 0:
            return [self.get_default_size()]
        return self.productsize_set.all()

    def get_default_size(self):
        if len(self.productsize_set.all()) == 0:
            sz = ProductSize(product = self, description = 'ÚNICO')
            sz.save()
            return sz
        return self.productsize_set.all().first()

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

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    description = models.CharField(max_length = 100)

    def __str__(self):
        return self.description
