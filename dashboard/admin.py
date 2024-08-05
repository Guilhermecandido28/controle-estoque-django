from django.contrib import admin
from .models import Saidas

class Saida(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'data', 'valor')
    list_display_links = ['id', 'descricao']
    search_fields = ['descricao', 'id', 'data', 'valor']
    list_per_page = 20


admin.site.register(Saidas, Saida)
