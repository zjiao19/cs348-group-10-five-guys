from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse(render(request, 'index.html', context={}))


def menu(request):
    return HttpResponse(render(request, 'menu.html', context={}))

def cart(request):
    return HttpResponse(render(request, 'cart.html', context={}))
