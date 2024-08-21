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
from .publisher import RabbitMQPublisher
import json
from django.contrib.auth.decorators import login_required

lista_preco = []

@login_required
def venda(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça o login para acessar o sistema.')
        return redirect('login')
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
        print("Método POST recebido")
        cod_barras = request.POST.get('codigo_barras', None)
        print(f"Código de barras recebido: {cod_barras}")

        if cod_barras and len(cod_barras) == 13:
            print("Código de barras válido com 13 caracteres")
            filtro = CodBarrasFilter(request.POST, queryset=Estoque.objects.all())
            print("Filtro de código de barras aplicado")
            
            # Aplicar o filtro
            obj = filtro.qs.values('codigo_barras', 'descricao', 'tamanho', 'cor', 'venda')
            print(f"Resultados do filtro: {obj}")
            
            quantidade = request.POST.get('quantidade', None)
            print(f"Quantidade recebida: {quantidade}")
            
            desconto = request.POST.get('desconto', None)
            print(f"Desconto recebido: {desconto}")
            
            desconto_porcentagem = Decimal(desconto) / Decimal(100)
            print(f"Desconto convertido para porcentagem: {desconto_porcentagem}")
            
            if obj.exists():
                print("Objeto existe no estoque")
                for item in obj:
                    total = Decimal(int(quantidade)) * Decimal(item['venda'])
                    total = total - total * desconto_porcentagem  # Calcula o total
                    print(f"Total calculado para o item: {total}")
                    
                    item['total'] = total  # Adiciona o total ao dicionário do item
                    item['quantidade'] = quantidade
                    lista_preco.append(item)
                    print(f"Item adicionado à lista de preços: {item}")
                
                template_name = 'vendas/partials/_table.html'
                context = {'object': obj, 'filtro': filtro, 'quantidade': quantidade, 'desconto': desconto}
                print(f"Contexto enviado para o template: {context}")
                return render(request, template_name, context)
            else:
                print("Nenhum resultado encontrado no estoque")
                return JsonResponse({'success': False, 'message': 'Nenhum resultado encontrado'})
        else:
            print("O código de barras deve ter 13 caracteres")
            return HttpResponseBadRequest("O código de barras deve ter 13 caracteres")

    print("Método não permitido")
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


def salvar_venda(request):    
    if request.method == 'POST':
        try:
            print("Obtendo valores de 'lista_preco'")
            valores = [(item['codigo_barras'], item['descricao'], item['tamanho'], item['cor'], item['quantidade']) for item in lista_preco]
            descricao = [', '.join(tupla) for tupla in valores]
            descricao = '; '.join(descricao)
            print(f"Descrição gerada: {descricao}")
            
            vendedor_id = request.POST.get('vendedor') 
            print(f"Vendedor ID obtido: {vendedor_id}")
            
            vendedores = Vendedores.objects.get(id=vendedor_id)
            print(f"Vendedor obtido: {vendedores}")
            
            cliente_id = request.POST.get('cliente') 
            print(f"Cliente ID obtido: {cliente_id}")
        except ValueError:
            erro = 'Campos obrigatórios não preenchidos!'
            print(f"Erro: {erro}")
            messages.error(request, f'Venda não concluída! Por favor, atualize a página e tente novamente. Erro: {erro}')      
        
        try:
            cliente = Clientes.objects.get(pk=cliente_id)
            print(f"Cliente obtido: {cliente}")
        except Exception as e:
            print(f"Erro ao obter cliente: {e}")
            cliente = None       

        forma_pagamento = request.POST.get('radio')        
        print(f"Forma de pagamento obtida: {forma_pagamento}")

        data = datetime.now()       
        print(f"Data atual: {data}")
        
        total = sum(item['total'] for item in lista_preco)
        print(f"Total calculado: {total}")
        
        try:
            # Cria a venda no banco de dados
            print("Criando venda no banco de dados...")
            venda = Vendas.objects.create(
                descricao=descricao,
                cliente=cliente,
                forma_pagamento=forma_pagamento,
                data=data,
                total=total,
                vendedor=vendedores
            )
            print(f"Venda criada: {venda}")

            try:
                print("Iniciando geração do recibo...")
                recibo = {'descricao': [], 'tamanho': [], 'cor': [], 'venda': [], 'quantidade':[]}  # Inicializamos as strings como listas
                
                for item in lista_preco:
                    recibo['descricao'].append(item['descricao'])
                    recibo['tamanho'].append(item['tamanho'])
                    recibo['cor'].append(item['cor'])
                    recibo['venda'].append(item['venda'])
                    recibo['quantidade'].append(item['quantidade'])
                
                # Convertendo as listas para strings, unindo os valores com ', '
                recibo['descricao'] = ', '.join(recibo['descricao'])
                recibo['tamanho'] = ', '.join(recibo['tamanho'])
                recibo['cor'] = ', '.join(recibo['cor'])
                recibo['venda'] = ', '.join([f"R$ {venda:.2f}" for venda in recibo['venda']])
                recibo['quantidade'] = ', '.join(recibo['quantidade'])
                print(f"Recibo gerado: {recibo}")
                
            except Exception as e:
                print(f'Erro ao criar recibo: {e}')

            try:
                print("Serializando mensagem para RabbitMQ...")
                message = json.dumps({
                    "data": data.strftime('%d/%m/%Y %H:%M:%S'),
                    "vendedor": vendedores.nome,
                    "cliente": cliente.nome if cliente else "",
                    "forma_pagamento": forma_pagamento,
                    "total": float(total),
                    "recibo": recibo
                }).encode('latin1')
                print(f"Mensagem serializada: {message}")
            except Exception as e:
                print(f'Erro ao serializar mensagem: {e}')

            try:
                print("Criando RabbitMQPublisher...")
                publisher = RabbitMQPublisher()
                print("Publisher criado com sucesso.")
                publisher.send_message(message)
                print("Mensagem enviada para RabbitMQ.")
            except Exception as e:
                print(f"Erro ao enviar mensagem para o RabbitMQ: {e}")

            lista_preco.clear()
            print("Lista de preços limpa.")

            messages.success(request, 'A venda foi realizada com sucesso!')  

            return render(request, 'vendas/partials/_message.html')
        except Exception as e:
            print(f"Erro ao criar venda: {e}")
            lista_preco.clear()
            print("Lista de preços limpa.")
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


def recibo(request):
    recibo = Vendas.objects.last()
    recibo = recibo.descricao
    return JsonResponse({"recibo": recibo})