from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendedores, name='vendedores'),
    path('ver_vendedor/', views.ver_vendedor, name='ver_vendedor')
]