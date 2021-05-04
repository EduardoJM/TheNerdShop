from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render
import json

from .models import Product, Category
from .utils import db

def index(request):
    promotional = Product.objects.filter(
        discount_price__gt=0
    ).order_by('-created_date')[:5]
    context = {
        'promotional_items': promotional,
        'menu': db.get_toplevel_menu()
    }
    return render(request, 'shop/views/home.html', context)

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

class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'shop/views/product_detail.html'
    