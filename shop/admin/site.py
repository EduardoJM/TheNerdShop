from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse

class ShopAdminSite(AdminSite):
    site_header = 'TheNerdShop'
    enable_nav_sidebar = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('data/products/', self.admin_view(self.view_data_products))
        ]
        return my_urls + urls

    def view_data_products(self, request):
        #questions = Question.objects.filter(pub_date__lte=timezone.now())
        context = dict(
            self.each_context(request),
            #questions=questions
        )
        return TemplateResponse(request, 'admin/data/data_products.html', context)

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
                    }
                ],
            }
        ]
        return app_list