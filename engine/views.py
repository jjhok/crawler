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
    "nameAttr_of_inputTag1": "value",
    "nameAttr_of_inputTag2": "value",
    "validate selctor": "selector",
},
'''
    else :
        template = """
{
    "idXpath": "xpath",
    "id": "value",
    "pwdXpath": "xpath",
    "pwd": "value",
    "submitXpath": "xpath",
    "validate_selector": "selector"
}
        """

    return JsonResponse(template, safe=False)

def testLogin(request):
    data = json.loads(request.body)
    login = data.get('login')
    method = data.get('method')
    url = data.get('url')
    inputDict = data.get('inputDict')

    if method == 'bs4' : 
        if login == True:
            result = bs4Login(url, inputDict, test=True)
        else: 
            result = bs4Connect(url)
    else :
        result = selLogin(url, inputDict, test=True)
        
    return JsonResponse(result)