from django.contrib import admin
from .models import Clientes

class Cliente(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    list_display_links = ['id', 'nome']
    search_fields = ['id', 'nome']
    list_per_page = 20

admin.site.register(Clientes, Cliente)