import django_filters
from django import forms
from vendedores.models import EventoVenda
from vendas.models import Vendas

class TrocaVendedorFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='icontains', label='Data')
    produto = django_filters.CharFilter(lookup_expr='icontains', label= 'Produto')
    total = django_filters.NumberFilter(lookup_expr='exact', label='Total R$')   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})


    class Meta:
        model = EventoVenda
        fields = ['data', 'vendedor', 'total', 'produto']

class TrocaClienteFilter(django_filters.FilterSet):    
    data = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})


    class Meta:
        model = Vendas
        fields = ['cliente', 'data']

class TrocaVendaFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={'type': 'date'}
            ),
            
        ) 
    descricao = django_filters.CharFilter(lookup_expr='icontains', label='Descrição') 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                
        for name, field in self.filters.items():            
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})

    class Meta:
        model = Vendas
        fields = ['id', 'data', 'descricao']
