import django_filters
from estoque.models import Estoque

class CodBarrasFilter(django_filters.FilterSet):    
    codigo_barras = django_filters.CharFilter(lookup_expr='exact', label= 'Cód.Barras:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Código de Barras:', 'autofocus': '', 'hx-post': '/vendas/pesquisar_produto/', 'hx-target': '#lista_item', 'hx-trigger': 'keyup changed', 'hx-swap': 'beforeend'})

    class Meta:
        model = Estoque
        fields = ['codigo_barras']