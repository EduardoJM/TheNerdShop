import json
from django.contrib.admin import AdminSite
from django.urls import path, include
from django.template.response import TemplateResponse

from ..models import Product, Category
from ..data import products as products_data

material_icons = {
    'Loja': 'shopping_cart',
    'Category': 'label',
    'Transaction': 'receipt',
    'Relacionamento': 'question_answer',
    'Vendas': 'monetization_on',
    'TransactionItem': 'shopping_cart',
    'Product': 'shopping_basket',
    'Notification': 'notifications'
}

def update_icons(apps):
    for app in apps:
        name = app['name']
        if name in material_icons:
            app['icon'] = material_icons[name]
        for model in app['models']:
            name = model['object_name']
            if name in material_icons:
                model['icon'] = material_icons[name]
    return apps

class ShopAdminSite(AdminSite):
    site_header = 'TheNerdShop'
    enable_nav_sidebar = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('data/', self.admin_view(self.view_data_index), name = 'data_index'),
            path('data/products/', self.admin_view(self.view_data_products), name = 'data_products'),
            path('data/abc-curve/', self.admin_view(self.view_abc_curve), name = 'data_abc'),
            path('crm/', include('crm.urls'))
        ]
        return my_urls + urls

    def view_data_index(self, request):
        context = dict(
            **self.each_context(request),
        )
        return TemplateResponse(request, 'admin/data/index.html', context)

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
        app_list = update_icons(super().get_app_list(request))
        app_list += [
            {
                "name": "Monitoramento de Dados",
                "app_label": "data_monitoring",
                "app_url": "admin/data/",
                "icon": "insert_chart",
                "models": [
                    {
                        "name": "Produtos",
                        "object_name": "data_products",
                        "admin_url": "/admin/data/products",
                        "icon": "insert_chart",
                        "view_only": True,
                    },
                    {
                        "name": "Curva ABC",
                        "object_name": "abc_curve",
                        "admin_url": "/admin/data/abc-curve/",
                        "icon": "show_chart",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list