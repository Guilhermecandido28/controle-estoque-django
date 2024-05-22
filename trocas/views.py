from django.shortcuts import render
from .filters import TrocaVendedorFilter, TrocaClienteFilter, TrocaVendaFilter
from vendedores.models import EventoVenda
from vendas.models import Vendas


def trocas(request):
    template_name = 'trocas/trocas.html'
    filtro_vendedor = TrocaVendedorFilter()
    filtro_cliente = TrocaClienteFilter()
    filtro_venda = TrocaVendaFilter()
    context={'filtro_vendedor': filtro_vendedor, 'filtro_cliente': filtro_cliente, 'filtro_venda': filtro_venda}
    return render(request, template_name , context )


def pesquisa_por_vendedor(request):        
    filtro = TrocaVendedorFilter(request.POST, queryset=EventoVenda.objects.all())    
    object_vendedor = filtro.qs    
    context = {
        'object_vendedor': object_vendedor,
        'filtro': filtro,
        'object_cliente': [],              
    }    
    template_name = 'trocas/partials/_tabela_vendedor.html'    
    return render(request, template_name, context)
    

def pesquisa_por_cliente_e_venda(request):
    cliente_id = request.POST.get('cliente')
    data = request.POST.get('data')
    id_venda = request.POST.get('id')
    descricao = request.POST.get('descricao')

    filtros = {}
    if cliente_id:
        filtros['cliente_id'] = cliente_id
    if data:
        filtros['data'] = data
    if id_venda:
        filtros['id'] = id_venda
    if descricao:
        filtros['descricao__icontains'] = descricao

    filtro = TrocaVendaFilter(request.POST, queryset=Vendas.objects.filter(**filtros))
    object_cliente_e_venda = filtro.qs
    context = {
        'object_vendedor': [],
        'filtro': filtro,
        'object_cliente_e_venda': object_cliente_e_venda,
    }    
    template_name = 'trocas/partials/_tabela_cliente_venda.html'

    return render(request, template_name, context)
   


    
    
