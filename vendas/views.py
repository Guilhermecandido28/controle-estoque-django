from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from .filters import CodBarrasFilter, VendasFilter
from estoque.models import Estoque
from .models import Vendas, Caixa
from clientes.models import Clientes
from .forms import VendaForms, CaixaForms
from datetime import datetime, date
from vendedores.models import Vendedores

from .functions import ajustar_estoque
from django.db.models.aggregates import Sum
from decimal import Decimal

lista_preco = []

def venda(request):
    form = VendaForms()
    form_caixa = CaixaForms() 
    object_vendas = Vendas.objects.all()
    object_filter_vendas = Vendas.objects.select_related('descricao', 'cliente', 'data', 'total') 
    filter_vendas = VendasFilter(request.GET, queryset=object_filter_vendas) 
    
    # Verificando se há registros no caixa
    ultimo_caixa = Caixa.objects.last()
    
    # Verificando se há registros no caixa
    if ultimo_caixa:
        # Verificando se a data do último registro é diferente da data de hoje
        if ultimo_caixa.data != date.today():
            valor = 0  # Se não for da data de hoje, definir valor como 0
        else:
            valor = ultimo_caixa.valor_inicial  # Caso contrário, utilizar o valor do último registro
    else:
        valor = 0  # Se não houver registros no caixa, definir valor como 0  
    for item in object_vendas:
        item.descricao = item.descricao.replace(';', '<br>') 
    object = Estoque.objects.select_related('descricao').all()
    object_filter = CodBarrasFilter(request.GET, queryset=object)    
    context = {'filter': object_filter, 'form':form, 'object_venda': object_vendas, 'caixa_form': form_caixa, 'valor': valor, 'filtro_venda': filter_vendas}
    return render(request, 'vendas/venda.html', context)


def inserir_venda(request): 
    if request.method == 'POST':
        cod_barras = request.POST.get('codigo_barras', None)        
        if cod_barras and len(cod_barras) == 13:
            filtro = CodBarrasFilter(request.POST, queryset=Estoque.objects.all())
            # Aplicar o filtro
            obj = filtro.qs.values('codigo_barras', 'descricao', 'tamanho', 'cor', 'venda')               
            quantidade = request.POST.get('quantidade', None)
            if obj.exists():                
                for item in obj:               
                    total = int(quantidade) * item['venda']  # Calcula o total
                    item['total'] = total  # Adiciona o total ao dicionário do item
                    lista_preco.append(item)  
                                 
                template_name = 'vendas/partials/_table.html'    
                context = {'object': obj, 'filtro': filtro, 'quantidade':quantidade}        
                return render(request, template_name, context)
            else:
                return JsonResponse({'success': False, 'message': 'Nenhum resultado encontrado'})
        else:
            print("O código de barras deve ter 13 caracteres")
            return HttpResponseBadRequest("O código de barras deve ter 13 caracteres")

    return JsonResponse({'success': False, 'message': 'Método não permitido'})

    
    

def salvar_venda(request):    
    if request.method == 'POST':
             
       
        valores = [(item['codigo_barras'], item['descricao'], item['tamanho'], item['cor']) for item in lista_preco]
        descricao = [', '.join(tupla) for tupla in valores]
        descricao = '; '.join(descricao)
        
        vendedor_id = request.POST.get('vendedor')
        
        try:
            vendedores = Vendedores.objects.get(id=vendedor_id)
            vendedores.produtos_vendidos += len(lista_preco)
            vendedores.save()
        except:
            
            vendedores = None
        cliente_id = request.POST.get('cliente')
        
        try:
             cliente = Clientes.objects.get(pk=cliente_id)
        except Exception as e:
            
            cliente = None
        
        desconto = request.POST.get('desconto')
        
        
        if desconto == '':
            desconto = 0
        
        forma_pagamento = request.POST.get('radio')
        
        
        data = datetime.now()
        
        
        desconto_decimal = Decimal(str(desconto))
        
        total = sum(item['total'] for item in lista_preco)
        total = total - (total * desconto_decimal / Decimal(100))
        
        
        try:
            Vendas.objects.create(descricao=descricao, cliente=cliente, desconto=desconto, forma_pagamento=forma_pagamento, data=data, total=total, vendedor=vendedores)
            ajustar_estoque(lista_preco)            
            lista_preco.clear()            
            return HttpResponse(status=200)
        except Exception as e:
            print("Erro ao criar venda:", e)           
            # Redireciona para a página anterior (com mensagem de erro)
            return HttpResponseBadRequest("Erro de validação: {}".format(e))
        

def movimentacao_dia(request): 
    # Obtém a data de hoje
    hoje = date.today()    
    
    # Filtra os dados para pegar apenas os registros da data de hoje
    dados = Vendas.objects.filter(data=hoje).values('forma_pagamento').annotate(soma_total=Sum('total')).order_by('forma_pagamento')
    

    # Formata os dados
    dados_formatados = []
    for item in dados:
        forma_pagamento = item['forma_pagamento']
        soma_total = item['soma_total']
        
        dados_formatados.append({'forma_pagamento': forma_pagamento, 'soma_total': soma_total})
    
    
        
    return JsonResponse(dados_formatados, safe=False)

def caixa_valor_inicial(request):
    valor = request.POST.get('valor_inicial')       
    
    if request.method == 'POST':
        
        form = CaixaForms(request.POST)
        if form.is_valid():
            
            form.save()  # Salva os dados no banco de dados
        
        context = {'valor': valor}     
           
        return render(request, 'vendas/partials/caixa_valor_inicial.html', context)
   
        
   

def caixa_lancar_saida(request):

    if request.method == 'POST':
          
        ultimo_caixa = Caixa.objects.last()
        if ultimo_caixa:
              
            if ultimo_caixa.data == date.today():
                  
                saida_post = Decimal(request.POST.get('saida'))
                  
                ultimo_caixa.saida += saida_post
                  
                ultimo_caixa.save()
                valor = ultimo_caixa.saldo()
                context = {'valor': valor}
                return render(request, 'vendas/partials/caixa_valor_inicial.html', context)
            
def pesquisar_vendas(request):
    filtro = VendasFilter(request.POST, queryset=Vendas.objects.all())
    object_vendas = filtro.qs
    template_name = 'vendas/partials/_table_vendas.html'    
    context = {'object_venda': object_vendas, 'filtro': filtro}        
    return render(request, template_name, context)



                  

            
   
               




    

