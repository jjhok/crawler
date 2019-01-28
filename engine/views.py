from django.shortcuts import render
from django.http import JsonResponse
import json
import asyncio

from .crawler_bs4 import *
from .crawler_selenium import *
from .html_parser import *
# from .crawler_bs4 import *
# from .crawler_selenium import *

# Create your views here.
def test(request):
    sample = {'hello': 'world'}
    return JsonResponse(sample, safe=True)

def templateLogin(request):
    method = request.GET.get('method')
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

def templateDetailPage(request):
    method = request.GET.get('method')
    if method == 'bs4':
        template = '''
[
    {
        "index": "index1",
        "selector" : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        "startAt": 0,
        "attr" : "data-role",
        "limit" : -1(ALL),
        "filterAttr" : "",
        "filterValue" : "",
    },
]
'''
    else :
        template = """
{
    'selector' : selector,
    'startAt': startAt,
    'limit': limit,
    'waitingForXpath': xpath
    'clickXpath': xpath
},
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

async def _main(loop, sem, urls, selectorDictList, nameSelector=None, loginSession=None, driverForCookie=None):
    futures = [bs4SinglePage(loop, sem, url, nameSelector=nameSelector,  selectorDictList=selectorDictList, loginSession=loginSession, driverForCookie=None) for url in urls]
    rets = await asyncio.gather(*futures)
    return rets

def testNestedPage(request):
    data = json.loads(request.body)
    method = data.get('method')
    urls = data.get('urls')
    inputDict = data.get('inputDict')

    if method == 'bs4' : 
        loop = asyncio.new_event_loop()    
        sem = asyncio.Semaphore(10, loop=loop)
        result = loop.run_until_complete( _main(loop, sem, urls, inputDict) )
        loop.close()
    else :
        result = selLogin(url, inputDict, test=True)
        
    return JsonResponse(result, safe=False)

def utilsFullpath(request):
    data = json.loads(request.body)
    baseUrl = data.get('baseUrl')
    parsingUrls = data.get('parsingUrls')

    return JsonResponse(getFullPath(baseUrl, parsingUrls), safe=False)