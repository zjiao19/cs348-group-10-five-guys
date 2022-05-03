from django import template
from orders.models import Ingredient, Category

register = template.Library()

@register.filter
def is_hidden(request):
    dirs = request.path.split('/')
    return 'logIn' in dirs or 'register' in dirs

@register.filter
def path(request):
    return request.path.split('/')[1]

@register.filter
def other_categories(product):
    return [_ for _ in Category.objects.all() if _.id != product.category.id]

@register.filter
def unused_ingredients(product):
    used_ingredients = [_.ingredient for _ in product.recipe_set.all()]
    ingredients = Ingredient.objects.all().order_by('name')
    return [_ for _ in ingredients if _ not in used_ingredients]

@register.filter
def id_is(product, id):
    if isinstance(id, str) and id.isnumeric():
        id = int(id)
    return product.id == id

@register.filter
def ingredient_id(recipe):
    return recipe.ingredient.id

@register.filter
def ingredient_name(recipe):
    return recipe.ingredient.name

@register.filter
def ingredient_unit(recipe):
    return recipe.ingredient.unit

@register.filter
def ingredient_quantity(recipe):
    return f'{recipe.ingredient_quantity:.2f}'

@register.filter
def order_price(order):
    return round(sum([_.item.price*_.quantity for _ in order.iteminorder_set.all()]), 2)

@register.filter
def order_items(order):
    return order.iteminorder_set.all()
