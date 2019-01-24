from django.shortcuts import render
from django.http import JsonResponse
import json

from .crawler_bs4 import *
from .crawler_selenium import *
# from .crawler_bs4 import *
# from .crawler_selenium import *

# Create your views here.
def test(request):
    sample = {'hello': 'world'}
    return JsonResponse(sample, safe=True)

def templateLogin(request):
    method = request.GET.get('method')
    print(request.GET)
    if method == 'bs4':
        template = '''
        {
            "nameAttr_of_inputTag": "value",
            "nameAttr_of_inputTag": "value",
        }
        '''
    else :
        template = """
        {
            'idXpath': 'xpath',
            'id': 'value',
            'pwdXpath': 'xpath',
            'pwd': 'value',
            'submitXpath': 'xpath'
        }
        """

    return JsonResponse(template, safe=False)

def testLogin(request):
    data = json.loads(request.body)
    method = data.get('method')
    url = data.get('url')
    inputDict = data.get('inputDict')
    print(inputDict)
    if method == 'bs4' : 
        bs4Login(url, inputDict)
    else :
        selLogin(url, inputDict)
        
    return JsonResponse(data, safe=True)