from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def test(request):
    sample = {'hello': 'world'}
    return JsonResponse(sample, safe=True)

def testLogin(request):
    method = data.get('method')
    url = data.get('url')
    id = data.get('id')
    pwd = data.get('pwd')
    return JsonResponse(data, safe=True)