from django.contrib import admin
from .models import Tarefas

class Tarefa(admin.ModelAdmin):
    list_display = ('id', 'tarefa', 'status')
    list_display_links = ['id', 'tarefa']
    search_fields = ['id', 'tarefas', 'status']
    list_per_page = 20
    verbose_name_plural = 'Tarefas'

admin.site.register(Tarefas, Tarefa)