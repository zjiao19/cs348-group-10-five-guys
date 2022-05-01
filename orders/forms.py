from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Ingredient, Product, Recipe, User

class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

class ImageForm(forms.Form):
    image = forms.ImageField()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
