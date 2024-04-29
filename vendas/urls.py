from django.urls import path
from . import views


urlpatterns = [
    path('', views.venda, name='vendas'),
    path('pesquisar_produto/', views.inserir_venda, name='codigo_barras'), 
    path('salvar_venda/', views.salvar_venda, name='salvar_venda'),
]

