import json
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse

from ..models import Product, Category
from ..data import products as products_data

class ShopAdminSite(AdminSite):
    site_header = 'TheNerdShop'
    enable_nav_sidebar = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('data/products/', self.admin_view(self.view_data_products)),
            path('data/products/abc/', self.admin_view(self.view_abc_curve)),
        ]
        return my_urls + urls

    def view_data_products(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        products_by_categories = []
        for cat in categories:
            products_cat = Product.objects.filter(categories__id=cat.id)
            products_cat_output = []
            for prod in products_cat:
                products_cat_output += [
                    dict(
                        name = prod.name,
                        price = prod.price.__str__(),
                        discount_price = prod.discount_price.__str__(),
                    )
                ]
            products_by_categories += [
                dict(
                    category = dict(
                        id = cat.id,
                        text = cat.text,
                        icon = cat.icon.name,
                    ),
                    products = products_cat_output
                )
            ]
        context = dict(
            self.each_context(request),
            products = products,
            categories = categories,
            products_by_categories = json.dumps(products_by_categories),
        )
        return TemplateResponse(request, 'admin/data/data_products.html', context)

    def view_abc_curve(self, request):
        context = dict(
            **self.each_context(request),
            abc_data = json.dumps(products_data.get_products_purchase_quantity_price())
        )
        return TemplateResponse(request, 'admin/data/abc_curve.html', context)
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Monitoramento de Dados",
                "app_label": "data_monitoring",
                # "app_url": "/admin/test_view",
                "models": [
                    {
                        "name": "Produtos",
                        "object_name": "data_products",
                        "admin_url": "/admin/data/products",
                        "view_only": True,
                    },
                    {
                        "name": "Curva ABC",
                        "object_name": "abc_curve",
                        "admin_url": "/admin/data/products/abc/",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list