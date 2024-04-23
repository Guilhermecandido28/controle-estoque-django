from django.shortcuts import render, redirect
from .filters import CodBarrasFilter
from estoque.models import Estoque

lista_preco = []
def venda(request):
    object = Estoque.objects.select_related('descricao').all()
    object_filter = CodBarrasFilter(request.GET, queryset=object)    
    context = {'filter': object_filter}
    return render(request, 'vendas/venda.html', context)



def pesquisar_produtos(request): 
    
    if request.method == 'POST':
        # Obter os dados do formulário de pesquisa
        filtro = CodBarrasFilter(request.POST, queryset=Estoque.objects.all())       
        # Aplicar o filtro
        obj = filtro.qs.values('codigo_barras', 'descricao', 'tamanho', 'cor', 'venda')
        obj_venda = filtro.qs.values('venda')        
        quantidade = request.POST.get('quantidade', None)
        for item in obj_venda:
            lista_preco.append(float(item['venda'])*int(quantidade))        
        
                     
    template_name = 'vendas/partials/_table.html'    
    context = {'object': obj, 'filtro': filtro, 'quantidade':quantidade}        
    return render(request, template_name, context)


def atualiza_total(request):
    template_name = 'vendas/partials/_modal.html'
    total = float(sum(lista_preco))    
    context = {'total': total}
    return render(request, template_name, context)


    

