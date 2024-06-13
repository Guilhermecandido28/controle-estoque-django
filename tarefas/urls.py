from django.urls import path
from . import views


urlpatterns = [
    path('', views.tarefas, name='tarefas'),
    path('adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),
    path('eventos/', views.eventos, name='eventos'),
    path('tarefa_concluida/', views.marcar_concluida, name='marcar_concluida')
]