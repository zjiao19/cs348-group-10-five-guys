from django.shortcuts import render
from orders.models import Product, Ingredient, Recipe

def db_demo_menu(request):
    context = {
        'products': Product.objects.all,
    }
    return render(request, 'lyk_menu.html', context)

def index(request):
    return render(request, 'index.html', context={})

def menu(request):
    return render(request, 'menu.html', context={})

def cart(request):
    return render(request, 'cart.html', context={})

def orderHistory(request):
    return render(request, 'orderHistory.html', context={})

def message(request):
    return render(request, 'message.html', context={})

def stockManagement(request):
    return render(request, 'stockManagement.html', context={})
