from django.db import models

class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/products')

    def __str__(self):
        return self.alternative_text

    class Meta:
        verbose_name = 'Imagens de Produtos'
        verbose_name_plural = 'Imagens de Produtos'