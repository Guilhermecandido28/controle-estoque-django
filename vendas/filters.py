import django_filters
from estoque.models import Estoque
from .models import Vendas

class CodBarrasFilter(django_filters.FilterSet):    
    codigo_barras = django_filters.CharFilter(lookup_expr='exact', label= 'Cód.Barras:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Código de Barras:', 'autofocus': ''})

    class Meta:
        model = Estoque
        fields = ['codigo_barras']



class VendasFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains', label='Descrição:')
    cliente = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains', label='Cliente:')
    data = django_filters.DateFilter(lookup_expr='contains', label='Data:')
    total = django_filters.NumberFilter(lookup_expr='exact', label= 'Total:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})

    class Meta:
        model = Vendas
        fields = ['descricao', 'cliente', 'data', 'total']