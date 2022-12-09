from django.db import models
from django.utils.html import format_html
from datetime import datetime
from django_quill.fields import QuillField

from .category import Category

class Product(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = QuillField('Descrição')
    categories = models.ManyToManyField(Category, verbose_name = 'Categorias')
    created_date = models.DateTimeField('Data de Criação', default=datetime.now, blank=True)
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

    def real_price(self):
        if self.discount_price > 0:
            return self.discount_price
        return self.price

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

try:
    Product.categories.through._meta.verbose_name = 'Categoria'
    Product.categories.through._meta.verbose_name_plural = 'Categorias'
    Product.categories.through.category.field.verbose_name = 'Categoria'
except:
    pass

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete = models.CASCADE)
    image = models.ImageField('Foto', upload_to='images/products')

    def __str__(self):
        return 'Foto do Produto' + str(self.product)

    class Meta:
        verbose_name = 'Imagens de Produtos'
        verbose_name_plural = 'Imagens de Produtos'

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    description = models.CharField('Tamanho', max_length = 100)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Tamanho do Produto'
        verbose_name_plural = 'Tamanhos do Produto'
