# Generated by Django 4.0.3 on 2022-04-30 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_ingredient_category_alter_order_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredient_Category',
            new_name='IngredientCategory',
        ),
    ]
