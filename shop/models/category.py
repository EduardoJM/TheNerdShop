from django.db import models

class Category(models.Model):
    text = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='images/icons/tags')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'