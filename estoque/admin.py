from django.contrib import admin
from .models import Estoque, MarcaEstoque, CategoriaEstoque

class Estoques(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'categoria', 'cor', 'tamanho', 'quantidade', 'venda')
    list_display_links = ['id', 'descricao', 'categoria', 'cor', 'tamanho', 'quantidade', 'venda']
    search_fields = ['descricao', 'categoria', 'cor', 'tamanho', 'quantidade', 'venda']
    list_per_page = 20


admin.site.register(Estoque, Estoques)

class Marcas(admin.ModelAdmin):
    list_display = ('id', 'marca',)
    list_display_links = ['id', 'marca']
    search_fields = ['id', 'marca']
    list_per_page = 20

admin.site.register(MarcaEstoque, Marcas)

class Categorias(admin.ModelAdmin):
    list_display = ('id', 'categoria',)
    list_display_links = ['id','categoria']
    search_fields = ['id', 'categoria']
    list_per_page = 20

admin.site.register(CategoriaEstoque, Categorias)


