from django.contrib import admin
from .models import Clientes, Eventos

class Cliente(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    list_display_links = ['id', 'nome']
    search_fields = ['id', 'nome']
    list_per_page = 20

admin.site.register(Clientes, Cliente)

class Evento(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento',)
    list_display_links = ['titulo']
    search_fields = [ 'titulo', 'data_evento' ]
    list_per_page = 20

admin.site.register(Eventos,  Evento)