from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserCreationForm, UserChangeForm
from .models import *

class UserAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

admin.site.register(User, UserAdmin)
admin.site.register(Product)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit')
admin.site.register(Ingredient, IngredientAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'ingredient_quantity')
admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Category)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'is_complete')
admin.site.register(Order, OrderAdmin)

class ItemInOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')
admin.site.register(ItemInOrder, ItemInOrderAdmin)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('staff', 'message')
admin.site.register(Alert, AlertAdmin)