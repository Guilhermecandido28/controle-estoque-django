from . import views, htmx_views
from django.urls import path


urlpatterns = [
    path('', views.clientes, name='clientes'),
    
    ] 

htmx_urlpatterns = [
    path('add_cliente', htmx_views.addcliente, name='addcliente'),
    path('update_cliente', htmx_views.update_cliente, name='updatecliente'),
    path('<int:id>/deletar_cliente/', htmx_views.deletar_cliente, name='deletar_cliente'),
    path('editar_cliente/<int:id>', htmx_views.editar_cliente, name='editar_cliente'),
    path('update_edicao/<int:id>', htmx_views.update_edicao, name='update_edicao'),
    path('last_cliente/', htmx_views.ultimo_cliente, name='last_cliente'),
    path('resultado_pesquisa/', htmx_views.pesquisar_cliente, name='pesquisar_cliente'),
    path('ver_cliente/<int:id>', htmx_views.ver_cliente, name='ver_cliente')
      
]

urlpatterns += htmx_urlpatterns