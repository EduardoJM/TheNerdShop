from django.http import HttpResponse
from django.views import generic
import json

from .models import Product, Category
from .utils import db

def index(request):
    return HttpResponse('Hello World!')

class CategoryProducts(generic.ListView):
    model = Product
    template_name = 'shop/views/products.html'
    paginate_by = 4
    ordering = ['-created_date']

    def get_queryset(self):
        return Product.objects.filter(categories__id=self.kwargs['category_id'])
    
    def get_context_data(self, **kwargs):
        context = super(CategoryProducts, self).get_context_data(**kwargs)
        context['menu'] = db.get_toplevel_menu()
        return context

class AllProducts(generic.ListView):
    model = Product
    template_name = 'shop/views/products.html'
    paginate_by = 4
    ordering = ['-created_date']

    def get_context_data(self, **kwargs):
        context = super(AllProducts, self).get_context_data(**kwargs)
        context['menu'] = db.get_toplevel_menu()
        return context