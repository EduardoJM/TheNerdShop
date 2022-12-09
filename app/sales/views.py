from django.conf import settings
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import redirect

import requests
from xml.etree import ElementTree

from .models import Transaction

def transaction_update(request, code):
    PAGSEGURO_BASE_URL3 = settings.PAGSEGURO_BASE_URL3
    PAGSEGURO_EMAIL = settings.PAGSEGURO_EMAIL
    PAGSEGURO_TOKEN = settings.PAGSEGURO_TOKEN
    if not PAGSEGURO_BASE_URL3 or not PAGSEGURO_EMAIL or not PAGSEGURO_TOKEN:
        raise HttpResponseServerError()

    url = PAGSEGURO_BASE_URL3 + 'transactions/' + code + '?email=' + PAGSEGURO_EMAIL + '&token=' + PAGSEGURO_TOKEN
    response = requests.get(url)
    if response.status_code == 200:
        tree = ElementTree.fromstring(response.text)
        Transaction.objects.filter(code = code).update(transaction_status = int(tree.find('status').text))
        return redirect('admin:sales_transaction_changelist')
    
    return HttpResponseServerError()

def transaction_notification(request):
    print(request)
    return HttpResponse('oie')
