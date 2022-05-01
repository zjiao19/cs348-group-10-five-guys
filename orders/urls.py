from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<next>\w*)/logIn$', views.logIn, name='logIn'),
    re_path(r'^(?P<next>\w*)/logOut$', views.logOut, name='logOut'),
    re_path(r'^(?P<next>\w*)/register$', views.register, name='register'),
    path('menu', views.menu, name='menu'),
    path('cart', views.cart, name='cart'),
    path('orderHistory', views.orderHistory, name='orderHistory'),
    path('message', views.message, name='message'),
    path('stockManagement', views.stockManagement, name='stockManagement'),
    path('productManagement', views.productManagement, name='productManagement'),
    re_path(r'^productManagement/(?P<id>\d*)$', views.productManagement, name='productManagement'),
]
