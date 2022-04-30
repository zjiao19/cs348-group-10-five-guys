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
            # for ingredient_id in ingredient_required:
            # update stock
            # if low insert message
            # if failed return alert
            # if success update order status
            # current_order.is_complete = True
            # current_order.save()
        if post['action'][0] == "Place Order":
            return redirect("/cart")
            return redirect("/orderHistory")
        else:
            return redirect("/cart")
    return render(request, 'cart.html', context=context)


def orderHistory(request):
    return render(request, 'orderHistory.html', context={})

def message(request):
    return render(request, 'message.html', context={})

def stockManagement(request):
    return render(request, 'stockManagement.html', context={})
