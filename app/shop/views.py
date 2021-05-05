from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import json

from .models import Product, Category
from .utils import db

from .forms.auth import UserCreationForm

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
    
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('shop:sign_in')
    
    context = {
        'form': form,
    }
    return render(request, 'auth/signup.html', context)

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('shop:index')
        else:
            messages.info(request, 'Usuário ou senha incorretos!')
    
    context = {}
    return render(request, 'auth/signin.html', context)

def sign_out(request):
    logout(request)
    return redirect('shop:sign_in')