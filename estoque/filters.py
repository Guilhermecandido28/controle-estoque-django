import django_filters
from .models import Estoque

class EstoqueFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains', label='Descrição:')
    cor = django_filters.CharFilter(lookup_expr='icontains', label='Cor:')
    venda = django_filters.CharFilter(lookup_expr='contains', label='Venda:')
    codigo_barras = django_filters.CharFilter(lookup_expr='icontains', label= 'Cód.Barras:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})

    class Meta:
        model = Estoque
        fields = ['descricao', 'categoria_id', 'marca_id']
