from django.contrib import admin
from .models import Vendedores

class Vendedor(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    list_display_links = ['id', 'nome']
    search_fields = ['id', 'nome']
    list_per_page = 20
    verbose_name_plural = 'Vendedores'

admin.site.register(Vendedores, Vendedor)
