from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from orders.models import *
from psycopg2 import sql
from .forms import *
from django.db.models import Sum
def index(request):
    return render(request, 'index.html', context={})

def menu(request):
    context = {
            'price': Product.objects.get(id=1).price,
            'products': Product.objects.all()
    }
    if request.method == 'POST':
        context['added_to_cart'] = request.POST['quantity']
    return render(request, 'menu.html', context=context)


def cart(request):
    return render(request, 'cart.html', context={})

def orderHistory(request):
    context = {
        'orders': list(Order.objects.filter(customer=request.user.id)),
        'selected': 'date'
    }
    if request.method == 'POST':
        if request.POST['order'] == 'price':
            for i in range(len(context['orders'])):
                context['orders'][i].price = sum([_.item.price*_.quantity for _ in context['orders'][i].iteminorder_set.all()])
            context['orders'].sort(key=lambda _: _.price)
            context['selected'] = 'price'
        else:
            context['orders'] = Order.objects.filter(customer=request.user.id).order_by('date')
    return render(request, 'orderHistory.html', context=context)

@login_required(login_url = "/")
def message(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM orders_alert where id = %s""", [request.POST['message_id']])
        else:
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE orders_alert set is_read = True where id = %s""", [request.POST['message_id']])
    context = {
            'messages': Alert.objects.filter(staff=request.user.id)
            }
    return render(request, 'message.html', context=context)

def stockManagement(request):
    return render(request, 'stockManagement.html', context={})

def updateProductImage(request, id):
    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid(): return
    product = Product.objects.get(id=id)
    product.image = form.cleaned_data['image']
    product.save()

def updateProductInfo(request, id):
    with connection.cursor() as cursor:
        for k, v in request.POST.items():
            if k == 'csrfmiddlewaretoken': continue
            args = k.split('|')
            args.insert(2, v)
            args.append(v)
            cursor.execute(f'''
                UPDATE orders_{args[0]} SET {args[1]} = %s
                WHERE id = %s AND {args[1]} IS DISTINCT FROM %s
            ''', args[2:])

def productManagement(request, id):
    if request.method == 'POST':
        if request.FILES:
            updateProductImage(request, id)
        else:
            updateProductInfo(request, id)
    context = {
            'products': Product.objects.all(),
            'current_product_id': int(id),
            'form': ImageForm(),
    }
    with open('form.log', 'w') as f:
        f.write(f'{context["form"]}\n{context["form"].as_p()}')
    return render(request, 'productManagement.html', context=context)

def logIn(request, next):
    context = {
            'next': next,
    }
    if request.method == 'GET':
        return render(request, 'logIn.html', context=context)
    context['username'] = request.POST.get('username')
    user = authenticate(username=context['username'], password=request.POST.get('password'))
    if user is None or not user.is_active:
        return render(request, 'logIn.html', context=context)
    login(request, user)
    return redirect(next if next else '/')

def logOut(request, next):
    logout(request)
    return redirect(next if next else '/')

def register(request, next):
    if request.method == 'GET':
        return render(request, 'register.html', context={'form': UserCreationForm()})
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, 'register.html', context={'form': form})
    form.save()
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect(next if next else '/')

