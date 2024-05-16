import django_filters
from .models import Vendedores

class VendedorFilter(django_filters.FilterSet):
    nome = django_filters.ChoiceFilter(choices=[], label='Selecione um Vendedor')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nomes = [(vendedor.nome, vendedor.nome) for vendedor in Vendedores.objects.all()]
        self.filters['nome'].extra['choices'] = nomes
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})


    class Meta:
        model = Vendedores
        fields = ['nome']
