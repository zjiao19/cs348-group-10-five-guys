from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
       return self.name

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=16, decimal_places=4)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    def __str__(self):
       return self.name

class IngredientCategory(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
       return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=8, decimal_places=4)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)
    unit = models.CharField(max_length=64)
    def __str__(self):
       return self.name

class Recipe(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.SET_NULL, null=True)
    ingredient_quantity = models.DecimalField(max_digits=8, decimal_places=4)
    def __str__(self):
       return "#{} {}".format(self.id, self.product)

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_complete = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
       return "#{} {}".format(self.id, self.customer)

class ItemInOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    def __str__(self):
       return "#{} {}".format(self.order, self.item)

class Alert(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, on_delete=models.CASCADE)
    is_read = models.BooleanField()
    message = models.TextField()
    def __str__(self):
       return str(self.id)
