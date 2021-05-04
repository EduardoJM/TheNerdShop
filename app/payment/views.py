from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from xml.etree import ElementTree
import requests
import xml
import json

def getSessionId(text):
    tree = ElementTree.fromstring(text)
    id_element = tree.getchildren()
    return id_element[0].text

def paymentAuth(request):
    PAGSEGURO_BASE_URL = settings.PAGSEGURO_BASE_URL
    PAGSEGURO_EMAIL = settings.PAGSEGURO_EMAIL
    PAGSEGURO_TOKEN = settings.PAGSEGURO_TOKEN
    if not PAGSEGURO_BASE_URL or not PAGSEGURO_EMAIL or not PAGSEGURO_TOKEN:
        raise HttpResponseBadRequest()
    url = PAGSEGURO_BASE_URL + 'sessions?email=' + PAGSEGURO_EMAIL + '&token=' + PAGSEGURO_TOKEN
    result = requests.post(url)
    if result.status_code == 200:
        result_json = {
            'id': getSessionId(result.text),
        }
        return HttpResponse(json.dumps(result_json), content_type="application/json")
    raise HttpResponseBadRequest()