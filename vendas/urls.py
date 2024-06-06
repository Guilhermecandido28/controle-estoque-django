from django.urls import path
from . import views


urlpatterns = [
    path('', views.venda, name='vendas'),
    path('pesquisar_produto/', views.inserir_venda, name='codigo_barras'), 
    path('salvar_venda/', views.salvar_venda, name='salvar_venda'),
    path('movimentacao_dia/', views.movimentacao_dia, name='movimentacao_dia'),
    path('abrir_caixa/', views.caixa_valor_inicial, name='abrir_caixa'),
    path('lanca_saida/', views.caixa_lancar_saida, name='lancar_saida'),
    path('pesquisar_venda/', views.pesquisar_vendas, name='pesquisar_venda'),
    path('deletar_venda/<int:id>', views.deletar_venda, name='deletar_venda'),
    path('card_troca/<int:id>', views.card_troca, name='card_troca'),
    path('produto_trocado/', views.produto_trocado, name='produto_trocado'),
    path('produto_novo/', views.produto_novo, name='produto_novo'),
    path('finalizar_troca/', views.finalizar_troca, name='finalizar_troca')
]

