from django.contrib import admin
from django.utils.html import format_html
from django.urls.base import reverse

from image_uploader_widget.admin import ImageUploaderInline

from ..models import Product, ProductSize, ProductImage
from ..forms.admin_shop import ProductForm, CategoryForm
from ..forms.action import ActionForm
from ..utils.values import brl

class ProductImageInline(ImageUploaderInline):
    model = ProductImage

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through

class ProductSizeInline(admin.TabularInline):
    model = ProductSize

class ProductAdmin(admin.ModelAdmin):
    action_form = ActionForm
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
    action_form = ActionForm
    form = CategoryForm
    fields = [
        'text',
        'icon',
        'parent',
        'top_menu',
    ]
    list_display = ['text', 'the_icon', 'parent', 'top_menu']
    list_filter = ['parent', 'top_menu']
    
    def the_icon(self, obj):
        return format_html('<img src="%s" alt="Ícone" style="width: 80px; height: auto;" />' % obj.icon.url)
    the_icon.short_description = 'Ícone'