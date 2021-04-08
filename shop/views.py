from django.http import HttpResponse
from django.views import generic

from .models import Product

def index(request):
    return HttpResponse('Hello World!')

class AllProducts(generic.ListView):
    model = Product
    template_name = 'shop/views/products.html'
    paginate_by = 2
    ordering = ['-created_date']
