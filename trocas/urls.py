from django.urls import path
from . import views

urlpatterns = [
    path('', views.trocas, name='trocas'),
    path('pesquisa_por_vendedor', views.pesquisa_por_vendedor, name='pesquisa_por_vendedor'),
    path('pesquisa_por_cliente', views.pesquisa_por_cliente_e_venda, name='pesquisa_por_cliente_e_venda'), 
      

]