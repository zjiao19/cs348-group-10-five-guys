from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('cart', views.cart, name='cart'),
    path('orderHistory', views.orderHistory, name='orderHistory'),
    path('message', views.message, name='message'),
    path('stockManagement', views.stockManagement, name='stockManagement'),
]
