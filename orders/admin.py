from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Order)
admin.site.register(ItemInOrder)
admin.site.register(Alert)