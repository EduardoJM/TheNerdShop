from django.http import HttpResponse, HttpResponseServerError
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings

import requests

from .forms.auth import UserUpdateForm
from .models import Product, ProductSize, CartProduct
from .utils import db, reference
from sales.models import Transaction

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

def cart(request):
    if not request.user.is_authenticated:
        return redirect('shop:index')

    cart = request.user.get_cart()
    items = cart.get_cart_items()
    context = {
        'cart': cart,
        'cart_items': items,
    }
    return render(request, 'shop/views/cart.html', context)

def cart_confirm(request):
    if request.method != 'POST':
        return redirect('shop:user_cart')
    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = '/'
    if not referer.endswith('/cart/'):
        return redirect('shop:user_cart')
    if not request.user.is_authenticated:
        return redirect('shop:index')

    cart = request.user.get_cart()
    items = cart.get_cart_items()
    context = {
        'cart': cart,
        'cart_items': items,
    }
    return render(request, 'shop/views/cart_confirm.html', context)

def cart_payment(request):
    if not request.user.is_authenticated:
        return redirect('shop:index')
    if request.method != 'POST':
        return redirect('shop:index')

    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = '/'

    if referer.endswith('/cart/user/update/'):
        form = UserUpdateForm(request.POST or None, instance = request.user)
        if form.is_valid():
            form.save()
    elif not referer.endswith('/cart/payment/'):
        return redirect('shop:user_cart')

    cart = request.user.get_cart()
    if referer.endswith('/cart/payment/'):
        print(request.POST)

        PAGSEGURO_BASE_URL = settings.PAGSEGURO_BASE_URL
        PAGSEGURO_EMAIL = settings.PAGSEGURO_EMAIL
        PAGSEGURO_TOKEN = settings.PAGSEGURO_TOKEN
        if not PAGSEGURO_BASE_URL or not PAGSEGURO_EMAIL or not PAGSEGURO_TOKEN:
            raise HttpResponseServerError()
        
        serialized_items = cart.serialize_cart()
        sender_email = request.user.email if settings.PAGSEGURO_ENV != 'SANDBOX' else 'test_the_nerd_shop@sandbox.pagseguro.com.br'
        method = request.POST.get('payment-method')
        if method != 'creditCard' and method != 'boleto':
            # TODO: render the same page with an error message
            return HttpResponseServerError()
        if method == 'creditCard':
            credit_card_payload = {
                'creditCardToken': request.POST.get('credit_card_token'),
                'installmentQuantity': request.POST.get('installments_quantity'),
                'installmentValue': "%.2f" % float(request.POST.get('installment')),
                'noInterestInstallmentQuantity': 3,
                'creditCardHolderName': request.POST.get('credit_card_name'),
                'creditCardHolderCPF': str(request.POST.get('credit_card_cpf')).replace('-', '').replace('.', ''),
                'creditCardHolderBirthDate': request.POST.get('credit_card_birth_date'),
                'creditCardHolderAreaCode': request.POST.get('credit_card_phone_code'),
                'creditCardHolderPhone': str(request.POST.get('credit_card_phone_number')).replace('-', ''),
                'billingAddressStreet': request.user.billing_address_street,
                'billingAddressNumber': request.user.billing_address_number,
                'billingAddressComplement': request.user.billing_address_complement,
                'billingAddressDistrict': request.user.billing_address_district,
                'billingAddressPostalCode': request.user.billing_address_postal_code,
                'billingAddressCity': request.user.billing_address_city,
                'billingAddressState': request.user.billing_address_state,
                'billingAddressCountry': request.user.billing_address_country,
            }
        else:
            credit_card_payload = {}
        boleto_payload = {}
        payload = {
            'paymentMode': 'default',
            'paymentMethod': method, # RECEIVE FROM POST
            'receiverEmail': 'eduardo_y05@outlook.com',
            'currency': 'BRL',
            **serialized_items,
            'extraAmount': '0.00',
            'reference': reference.get_new_ref(),
            'senderName': request.user.first_name + ' ' + request.user.last_name,
            'senderCPF': request.user.cpf,
            'senderAreaCode': request.user.phone_code,
            'senderPhone': request.user.phone_number,
            'senderEmail': sender_email,
            'senderHash': request.POST.get('user_hash_token'),
            **(credit_card_payload if method == 'creditCard' else {}),
            **(boleto_payload if method == 'boleto' else {}),
            # TODO: change the below settings if shipping used
            'shippingAddressRequired': False,
            # TODO: change this to use the webhooks for notification
            #'notificationURL': 'https://teste.institutoinventare.com.br/notification',
        }
        #print(payload)
        url = PAGSEGURO_BASE_URL + 'transactions?email=' + PAGSEGURO_EMAIL + '&token=' + PAGSEGURO_TOKEN
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
        response = requests.post(url, data = payload, headers = headers)
        if response.status_code == 200:
            transaction = Transaction()
            transaction.parse_values_from_xml(response.text, cart)
            return redirect('shop:index')
        print (response.text)
        # TODO: render the same page with an error message
        return HttpResponseServerError()

    items = cart.get_cart_items()
    context = {
        'cart': cart,
        'cart_items': items,
    }
    return render(request, 'shop/views/cart_payment.html', context)

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('shop:index')
    if request.method != 'POST':
        return redirect('shop:index')
    
    product_id = request.POST['product_id']
    size = request.POST.get('size', None)
    quantity = int(request.POST['quantity'])
    
    prod = Product.objects.filter(pk = product_id).first()
    if prod is None:
        return redirect('shop:user_cart')

    if size is None:
        size = 'ÚNICO'
    size_obj = ProductSize.objects.filter(description = size).first()
    
    cart = request.user.get_cart()
    cart.add_to_cart(prod, quantity, size_obj)

    return redirect('shop:user_cart')

def remove_from_cart(request, register_id):
    if not request.user.is_authenticated:
        return redirect('shop:index')
    
    cart = request.user.get_cart()
    prod_item = CartProduct.objects.filter(pk = register_id, cart = cart)

    if prod_item is None:
        return redirect('shop:user_cart')
    
    prod_item.delete()

    return redirect('shop:user_cart')

def cart_update_user(request):
    if not request.user.is_authenticated:
        return redirect('shop:index')
    if request.method != 'POST':
        return redirect('shop:user_cart')
    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = '/'
    if not referer.endswith('/cart/confirm/'):
        return redirect('shop:user_cart')
    context = {}
    return render(request, 'shop/views/cart_update_user.html', context)

def purchases_list(request, id = None):
    if not request.user.is_authenticated:
        return redirect('shop:index')
    if id is None:
        context = {
            'purchases': Transaction.objects.filter(sender = request.user).all().order_by('-date')
        }
        return render(request, 'shop/views/purchases_list.html', context)
    else:
        transaction = Transaction.objects.filter(pk = id).first()
        if transaction is None:
            return redirect('shop:purchases_list')
        context = {
            'purchase': transaction
        }
        return render(request, 'shop/views/purchases_description.html', context)
