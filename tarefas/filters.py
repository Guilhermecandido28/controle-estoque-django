import django_filters
from .models import Tarefas
from vendedores.models import Vendedores




class TarefasFilter(django_filters.FilterSet):
    tarefa = django_filters.CharFilter(lookup_expr='icontains', label='Descrição:')
    funcionario = django_filters.ModelChoiceFilter(
        field_name='funcionario__id',
        queryset=Vendedores.objects.all(),
        to_field_name='id',
        label='Funcionários',        
    )
    inicio = django_filters.DateFilter(lookup_expr='contains', label='Data de Início:')
    prazo = django_filters.DateFilter(lookup_expr='contains', label='Prazo:')
    status = django_filters.BooleanFilter(label='Status:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.filters.items():
            field.field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})

    class Meta:
        model = Tarefas
        fields = ['tarefa', 'funcionario', 'inicio', 'prazo', 'status']