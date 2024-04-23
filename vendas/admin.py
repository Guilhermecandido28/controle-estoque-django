from django.contrib import admin
from .models import Vendas

class Venda(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'total', 'cliente')
    list_display_links = ['id', 'descricao']
    search_fields = ['descricao', 'id', 'total', 'cliente']
    list_per_page = 20


admin.site.register(Vendas, Venda)
