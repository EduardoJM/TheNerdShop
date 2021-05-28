from django.contrib import admin

from ..models import Product, ProductImage, Category
from ..forms.admin_shop import ProductForm

class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 3

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through

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
        ProductImageInline,
        ProductCategoryInline
    ]

class ProductImageAdmin(admin.ModelAdmin):
    fields = [
        'alternative_text',
        'description',
        'image'
    ]

class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'text',
        'icon',
        'parent',
        'top_menu',
    ]