from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from orders.models import *
from psycopg2 import sql
from .forms import *
from django.db.models import Sum
import json
def index(request):
    return render(request, 'index.html', context={})

@login_required(login_url='/menu/logIn')
def menu(request):
    context = {
            'price': Product.objects.get(id=1).price,
            'products': Product.objects.all()
    }
    post = dict(request.POST)
    quantity = 0,
    item = ''
    for key, value in post:
        if 'quantity' in key:
            item = key.split('_')[1]
            quantity = int(value)
    # Insert new order
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("BEGIN"))
        cursor.execute(sql.SQL("COMMIT"))




    with open('menu.log','w') as f:
        f.write(json.dumps(request.POST))
    return render(request, 'menu.html', context=context)


@login_required(login_url='/cart/logIn')
def cart(request):
    current_orders = Order.objects.filter(customer=request.user.id, is_complete = False) # test id
    context = {
        "empty": False
    }
    if len(current_orders) > 0:
        context['current_order'] = current_orders[0]
        context['items'] = ItemInOrder.objects.filter(order = current_orders[0])
    else:
        context['empty'] = True
    if request.method == 'POST':
        current_order = current_orders[0]
        post = dict(request.POST)
        for key in post:
            if 'quantity' in key:
                item_id = key.split('_')[1]
                ItemInOrder.objects.filter(order = current_order, item = item_id).update(quantity = post[key][0])
        if post['action'][0] == "Place Order":
            ingredient_required = dict()
            for item in current_order.iteminorder_set.all():
                for recipe in item.item.recipe_set.all():
                    ingredient_id = recipe.ingredient.id
                    quantity = recipe.ingredient_quantity * item.quantity
                    if ingredient_id in ingredient_required:
                        ingredient_required[ingredient_id] += quantity
                    else:
                        ingredient_required[ingredient_id] = quantity
            
            # start transaction
            ingredient_error, ingredient_warning = None, None
            with connection.cursor() as cursor:
                cursor.execute(sql.SQL("BEGIN"))
                cursor.execute(sql.SQL("""
                        UPDATE orders_order SET is_complete = True
                        WHERE id = %s
                """), [current_order.id])

                for ingredient_id, quantity in ingredient_required.items():
                    cursor.execute(sql.SQL("""
                        UPDATE orders_ingredient SET quantity = quantity - %s
                        WHERE id = %s"""), [quantity, ingredient_id])
                
                cursor.execute(sql.SQL("""
                    SELECT name FROM orders_ingredient
                    WHERE quantity < 0"""))
                ingredient_error = cursor.fetchall()
                print("error:" + str(ingredient_error))

                cursor.execute(sql.SQL("""
                    SELECT name FROM orders_ingredient
                    WHERE quantity < %s"""), [100])
                ingredient_warning = cursor.fetchall()
                print("warning:" + str(ingredient_warning))

                if len(ingredient_error) > 0:
                    cursor.execute(sql.SQL("ROLLBACK"))
                    context['error'] = "Error: Sorry, we don't have enough ingredients to complete your order."
                else:
                    cursor.execute(sql.SQL("COMMIT"))
            # insert message
            if 'error' in context:
                for ingredient in ingredient_error:
                    for staff in User.objects.filter(is_staff=True):
                        Alert.objects.create(
                            staff = staff,
                            is_read = False,
                            message = f"Low Stock ERROR: we don't have enough {ingredient[0]} to complete order #{current_order.id}."
                        )
            else:
                for ingredient in ingredient_warning:
                    for staff in User.objects.filter(is_staff=True):
                        Alert.objects.create(
                            staff = staff,
                            is_read = False,
                            message = f"Low Stock WARNING: we need more {ingredient[0]}."
                        )
        if post['action'][0] == "Place Order":
            if 'error' in context:
                return render(request, 'cart.html', context=context)
            return redirect("/orderHistory")
        else:
            return redirect("/cart")
    return render(request, 'cart.html', context=context)


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

@login_required(login_url='/productManagement/logIn')
def productManagement(request, id):
    if request.method == 'POST':
        if request.FILES:
            updateProductImage(request, id)
        else:
            updateProductInfo(request, id)
    context = {
            'ingredients': Ingredient.objects.all(),
            'products': Product.objects.all(),
            'current_product_id': int(id),
    }
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

