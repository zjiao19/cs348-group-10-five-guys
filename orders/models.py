from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
       return self.name

class Staff(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
       return self.name

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=16, decimal_places=4)
    def __str__(self):
       return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=8, decimal_places=4)
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
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    is_complete = models.BooleanField()
    def __str__(self):
       return self.id

class ItemInOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    def __str__(self):
       return "#{} {}".format(self.order, self.item)

class Alert(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    is_read = models.BooleanField()
    message = models.TextField()
    def __str__(self):
       return self.id
