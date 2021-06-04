from django.contrib import admin
from django.utils.html import format_html
from django.urls.base import reverse

from ..models import Product, ProductSize, ProductImage
from ..forms.admin_shop import ProductForm
from ..utils.values import brl

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through

class ProductSizeInline(admin.TabularInline):
    model = ProductSize

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    fields = [
        'name',
        'description',
        'created_date',
        'price',
        'discount_price'
    ]
    inlines=[
        ProductSizeInline,
        ProductImageInline,
        ProductCategoryInline
    ]
    list_display = ['the_image', 'name', 'created_date', 'the_price', 'the_categories']

    def the_image(self, obj):
        img = obj.productimage_set.first()
        return format_html('<img src="%s" alt="Foto de Preview" style="width: 150px; height: auto;" />' % img.image.url)
    the_image.short_description = 'Foto'

    def the_price(self, obj):
        return brl(obj.real_price())
    the_price.short_description = 'Preço Atual'

    def the_categories(self, obj):
        html = ''
        categories = obj.categories.all()
        for cat in categories:
            cat_html = '<a href="%s">%s</a>' % (
                reverse('admin:shop_category_change', args=[cat.id]),
                str(cat)
            )
            html = html + cat_html if html != '' else cat_html
        return format_html(html)
    the_categories.short_description = 'Categorias'

class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'text',
        'icon',
        'parent',
        'top_menu',
    ]