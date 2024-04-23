from django.urls import path
from . import views, htmx_views


urlpatterns = [
    path('', views.estoque, name='estoque'),    
    path('dados_grafico/', views.dados_grafico, name='dados_grafico'),
      
]

htmx_urlpatterns = [    
    path('salvar_produto/', htmx_views.salvar_produtos, name='salvar_produto'),
    path('<int:id>/deletar_produto/', htmx_views.deletar_produtos, name='deletar_produto'),
    path('<int:id>/', htmx_views.editar_produto, name= 'editar_produto'),
    path('<int:id>/update/', htmx_views.update_produto, name= 'update_produto'),
    path('pesquisar_produto/', htmx_views.pesquisar_produtos, name='pesquisar_produto'), 
    path('estoque_baixo/', htmx_views.estoque_baixo, name='estoque_baixo'),
    path('adicionar_categoria/', htmx_views.add_categoria, name='add_categoria'), 
    path('update_categoria/', htmx_views.update_categoria, name='update_categoria'),
    path('delete_categoria/', htmx_views.deletar_categoria, name='deletar_categoria'),
    path('adicionar_marca/', htmx_views.add_marca, name='add_marca'), 
    path('update_marca/', htmx_views.update_marca, name='update_marca'),
    path('delete_marca/', htmx_views.deletar_marca, name='deletar_marca'),
     
]


urlpatterns += htmx_urlpatterns