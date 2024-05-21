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
    # Imprimindo os dados recebidos na requisição POST
    print("Dados da requisição POST:", request.POST)
    
    # Criação do filtro com os dados da requisição e queryset inicial
    filtro = TrocaVendedorFilter(request.POST, queryset=Vendas.objects.all())    
    
    # Imprimindo o queryset inicial
    print("Queryset inicial (Vendas.objects.all()):", Vendas.objects.all())
    
    # Aplicação do filtro e obtenção do queryset filtrado
    object_cliente_e_venda = filtro.qs
    
    # Imprimindo o queryset após aplicação do filtro
    print("Queryset após aplicação do filtro (filtro.qs):", object_cliente_e_venda)
    
    # Definindo o contexto a ser passado para o template
    context = {
        'object_vendedor': [],
        'filtro': filtro,
        'object_cliente_e_venda': object_cliente_e_venda,
    }    
    
    # Imprimindo o contexto antes de renderizar o template
    print("Contexto para o template:", context)
    
    template_name = 'trocas/partials/_tabela_cliente_venda.html'

    # Renderizando o template com o contexto
    return render(request, template_name, context)

   


    
    
