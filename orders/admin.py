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
admin.site.register(Ingredient)

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

admin.site.register(Alert)

admin.site.register(Ingredient_Category)
