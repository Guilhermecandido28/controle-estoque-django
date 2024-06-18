from django.shortcuts import render, redirect
from estoque.forms import AddEstoqueForms
from .models import Estoque
from django.db.models.aggregates import Sum, Count
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from .filters import EstoqueFilter
from django.contrib.auth.decorators import login_required




@login_required
def estoque(request):
    if request.user.is_authenticated:
        
        object = Estoque.objects.select_related('categoria', 'marca').order_by('descricao').all().all() #pega apenas os campos que eu quero para ser colocado na tabela do arquivo html.
        object_filter = EstoqueFilter(request.GET, queryset=object)
        form = AddEstoqueForms()
        baixo_estoque = Estoque.objects.filter(quantidade__lte=1).aggregate(baixo_estoque=Count('quantidade'))  # verifica quantos produtos estão abaixo ou igual a zero.


        if object.exists():            
            total = Estoque.objects.aggregate(
                soma_total = Sum('venda'),
                soma_investimento = Sum('custo'),
                quantidade_produtos = Count('id')
                ) # faz a soma dos valores dos produtos e conta quantos produtos existem no banco de dados.
            
            context = {
            'object': object,
            'form': form,
            'contagem': total['quantidade_produtos'],
            'soma': total['soma_total'],
            'soma_invs': total['soma_investimento'],
            'baixo_estoque': baixo_estoque['baixo_estoque'],
            'filter': object_filter

        }
        else:            
            context = {
            'object': object,
            'form': form,
            'contagem': 0,
            'soma': 0,
            'soma_invs': 0,
            'baixo_estoque': 0,
            'filter': object_filter

        }
        
        
        

                
        return render(request, 'estoque/index_estoque.html', context) # renderiza os valores obtidos no arquivo html.
    else:
        messages.error(request, 'Faça o login para acessar o sistema.')
        return redirect('login')
    




def dados_grafico(request):
    dados = Estoque.objects.annotate(mes=TruncMonth('data')).values('mes').annotate(quantidade=Count('id')).order_by('mes')
    dados_formatados = {item['mes'].strftime('%b'): item['quantidade'] for item in dados}
    return JsonResponse(dados_formatados)

    

