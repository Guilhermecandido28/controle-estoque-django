from django.urls import path
from . import views


urlpatterns = [
    path('', views.venda, name='vendas'),
    path('pesquisar_produto/', views.pesquisar_produtos, name='codigo_barras'), 
    path('atualiza_total/', views.atualiza_total, name='atualiza_total'),
        
]

