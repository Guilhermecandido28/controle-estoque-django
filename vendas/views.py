from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from .filters import CodBarrasFilter, VendasFilter
from estoque.models import Estoque
from .models import Vendas, Caixa, Troca
from clientes.models import Clientes
from .forms import VendaForms, CaixaForms, TrocaForms
from datetime import datetime, date
from vendedores.models import Vendedores
from django.contrib import messages
from .functions import ajustar_estoque
from django.db.models.aggregates import Sum
from decimal import Decimal
import requests

lista_preco = []

def venda(request):
    form = VendaForms()
    form_caixa = CaixaForms() 
    object_vendas = Vendas.objects.all().order_by('-data')
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
            desconto = request.POST.get('desconto', None)
            desconto_porcentagem = Decimal(desconto) / Decimal(100)
            if obj.exists():                
                for item in obj:               
                    total = Decimal(int(quantidade)) * Decimal(item['venda'])
                    total = total - total*desconto_porcentagem   # Calcula o total
                    print(total)
                    item['total'] = total  # Adiciona o total ao dicionário do item
                    lista_preco.append(item) 
                template_name = 'vendas/partials/_table.html'    
                context = {'object': obj, 'filtro': filtro, 'quantidade':quantidade, 'desconto': desconto}        
                return render(request, template_name, context)
            else:
                return JsonResponse({'success': False, 'message': 'Nenhum resultado encontrado'})
        else:
            print("O código de barras deve ter 13 caracteres")
            return HttpResponseBadRequest("O código de barras deve ter 13 caracteres")

    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def salvar_venda(request):    
    if request.method == 'POST':
        try:
            valores = [(item['codigo_barras'], item['descricao'], item['tamanho'], item['cor']) for item in lista_preco]
            descricao = [', '.join(tupla) for tupla in valores]
            descricao = '; '.join(descricao)       
            vendedor_id = request.POST.get('vendedor')                
            vendedores = Vendedores.objects.get(id=vendedor_id)            
            cliente_id = request.POST.get('cliente')  
        except ValueError:
            erro = 'Campos obrigatórios não preenchidos!'
            messages.error(request, f'Venda não concluída! Por favor, atualize a página e tente novamente. Erro: {erro}')      
        try:
            cliente = Clientes.objects.get(pk=cliente_id)
        except Exception as e:            
            cliente = None
        

        
        forma_pagamento = request.POST.get('radio')        
        data = datetime.now()       
        
        total = sum(item['total'] for item in lista_preco)

        print(total)  
        
        try:
            # Cria a venda no banco de dados
            venda = Vendas.objects.create(
                descricao=descricao,
                cliente=cliente,
                forma_pagamento=forma_pagamento,
                data=data,
                total=total,
                vendedor=vendedores
            )
            ajustar_estoque(lista_preco)
            print(lista_preco)            

            # Gerar o texto do recibo
            recibo = "RECIBO DE VENDA\n"
            recibo += f"Data: {data.strftime('%d/%m/%Y %H:%M:%S')}\n"
            recibo += f"Vendedor: {vendedores.nome}\n"
            if cliente:
                recibo += f"Cliente: {cliente.nome}\n"
            recibo += "\nItens:\n"
            
            for item in lista_preco:
                recibo += f"{item['descricao']} ({item['tamanho']} - {item['cor']}) - R$ {item['total']:.2f}\n\n"
            

            recibo += f"Total: R$ {total:.2f}\n\n"
            recibo += f"Forma de Pagamento: {forma_pagamento}\n"
            recibo += "\nObrigado pela sua compra!\n"

            # Enviar a solicitação POST para a API de impressão
            url = "http://localhost:8001/api/print/"
            headers = {"Content-Type": "application/json"}
            payload = {"text": recibo}
            
            response = requests.post(url, headers=headers, json=payload)
            print(f"Resposta da API de impressão: {response.status_code} - {response.text}")
            lista_preco.clear()
            print(lista_preco)
            messages.success(request, 'A venda foi realizada com sucesso!')  

            return render(request, 'vendas/partials/_message.html')
        except Exception as e:
            lista_preco.clear()
            messages.error(request, f'A Venda falhou, erro: {e}')           
            return render(request, 'vendas/partials/_message.html')

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

def deletar_venda(request, id):
    template_name = 'vendas/partials/_table.html'
    global lista_preco
    id_str = str(id)
    lista_preco = [item for item in lista_preco if item['codigo_barras'] != id_str]    
              
    return render(request, template_name)


def card_troca(request, id):
    template_name = 'vendas/partials/trocas.html'
    form = TrocaForms()
    object = Vendas.objects.filter(id=id).values_list('descricao', flat=True)
    context = {'object': object, 'form': form, 'venda_id': id}
    return render(request, template_name, context)

def produto_trocado(request):
    if request.method == 'POST':
        produto_trocado = request.POST.get('produto_trocado')
        if produto_trocado and len(produto_trocado) == 13:
            produto = Estoque.objects.filter(codigo_barras = produto_trocado).values_list('codigo_barras','descricao', 'tamanho', 'cor', 'venda')
            template_name = 'vendas/partials/produto_trocado.html'
            context = {'produto': produto}
            return render(request, template_name, context)
        else:
            return HttpResponseBadRequest("O código de barras deve ter 13 caracteres")
    else:
        return HttpResponse("Método não permitido.", status=405)
    
def produto_novo(request):
    if request.method == 'POST':
        produto_novo = request.POST.get('produto_novo')
        if produto_novo and len(produto_novo) == 13:
            produto = Estoque.objects.filter(codigo_barras = produto_novo).values_list('codigo_barras','descricao', 'tamanho', 'cor', 'venda')
            template_name = 'vendas/partials/produto_novo.html'
            context = {'produto': produto}
            return render(request, template_name, context)
        else:
            return HttpResponseBadRequest("O código de barras deve ter 13 caracteres")
    else:
        return HttpResponse("Método não permitido.", status=405)
    
def finalizar_troca(request, id):
    venda = get_object_or_404(Vendas, id=id)  # Obtém a instância da venda
    produto_trocado = request.POST.get('produto_trocado')
    produto_novo = request.POST.get('produto_novo')
    objeto_trocado = get_object_or_404(Estoque, codigo_barras=produto_trocado)
    objeto_novo = get_object_or_404(Estoque, codigo_barras=produto_novo)

    # Atualizar a quantidade do objeto trocado
    objeto_trocado.quantidade -= 1
    objeto_trocado.save()

    # Atualizar a quantidade do objeto novo
    objeto_novo.quantidade += 1
    objeto_novo.save()

    diferenca = float(objeto_trocado.venda) - float(objeto_novo.venda) 

    Troca.objects.create(
        venda=venda,  # Passa a instância de Vendas
        produto_trocado=objeto_trocado,
        produto_novo=objeto_novo,
        valor_diferenca=diferenca*-1
    )

    object_vendas = Vendas.objects.all()
    template_name = 'vendas/partials/_table_vendas.html'
    context = {'object_venda': object_vendas}
    return render(request, template_name, context)


def cancelar_troca(request):
    template_name = 'vendas/partials/_table_vendas.html'
    object_vendas = Vendas.objects.all()
    context = {'object_venda': object_vendas}
    return render(request, template_name, context)