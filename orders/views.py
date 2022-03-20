from django.shortcuts import render
from orders.models import Product, Ingredient, Recipe

def menu(request):
    context = {
        'products': Product.objects.all,
    }
    return render(request, 'menu.html', context)
