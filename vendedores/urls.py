from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendedores, name='vendedores'),
    path('ver_vendedor/', views.ver_vendedor, name='ver_vendedor'),
    path('evento_venda_calendario/', views.eventos_venda_calendario, name='eventos_venda_calendario')

]