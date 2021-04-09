from django.contrib import admin
from django import forms

from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 3

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through

class ProductAdmin(admin.ModelAdmin):
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

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    fields = [
        'alternative_text',
        'description',
        'image'
    ]

admin.site.register(ProductImage, ProductImageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'text',
        'icon',
        'parent',
        'top_menu',
    ]

admin.site.register(Category, CategoryAdmin)
