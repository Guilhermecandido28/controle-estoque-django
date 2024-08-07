from django.urls import path
from . import views


urlpatterns = [
    path('', views.tarefas, name='tarefas'),
    path('adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),
    path('eventos/', views.eventos, name='eventos'),
    path('editar_tarefa/<int:id>', views.editar_tarefa, name='editar_tarefa'),
    path('apagar_tarefa/<int:id>', views.apagar_tarefa, name='apagar_tarefa'),
    path('ver_notificacao/', views.ver_notificacao, name='ver_notificacao'),
]