from django.shortcuts import render, redirect
from estoque.forms import AddEstoqueForms
from .models import Estoque, CategoriaEstoque
from django.db.models.aggregates import Sum, Count
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from .filters import EstoqueFilter
from django.contrib.auth.decorators import login_required




@login_required
def estoque(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça o login para acessar o sistema.')
        return redirect('login')

    # Deletar registros com quantidade = 0
    Estoque.objects.filter(quantidade=0).delete()
    
    # Consultar todos os dados necessários de uma vez
    queryset = Estoque.objects.all()
    total = queryset.aggregate(
        soma_total=Sum('venda'),
        soma_investimento=Sum('custo'),
        quantidade_produtos=Count('id')
    )
    
    baixo_estoque_count = queryset.filter(quantidade__lte=1).count()
    
    object_filter = EstoqueFilter(request.GET, queryset=queryset)
    form = AddEstoqueForms()
    
    context = {
        'object': queryset,
        'form': form,
        'qtd_produtos': total['quantidade_produtos'],
        'soma': total['soma_total'],
        'soma_invs': total['soma_investimento'],
        'baixo_estoque': baixo_estoque_count,
        'filter': object_filter
    }
    
    return render(request, 'estoque/index_estoque.html', context)
    

def dados_grafico(request):
    dados = Estoque.objects.annotate(mes=TruncMonth('data')).values('mes').annotate(quantidade=Count('id')).order_by('mes')
    dados_formatados = {item['mes'].strftime('%b'): item['quantidade'] for item in dados}
    return JsonResponse(dados_formatados)

    

