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
from django.utils import timezone
from django.core.exceptions import ValidationError
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



def pesquisar_produto(request):
    search_codigo_barras = request.GET.get('search_codigo_barras', '')    
    # Consultando o banco de dados com o código de barras
    produtos = Estoque.objects.filter(codigo_barras__exact=search_codigo_barras)
    
    results = []
    for produto in produtos:

        results.append({
            'codigo_barras': produto.codigo_barras,
            'descricao': produto.descricao,
            'tamanho': produto.tamanho,
            'cor': produto.cor,
            'preco': float(produto.venda),  # Convertendo Decimal para float
        })

    data = {'results': results}
    return JsonResponse(data)

        



def salvar_venda(request):
    if request.method == 'POST':
        try:
            # Coleta e imprime dados recebidos
            data = json.loads(request.body)
            print('Dados recebidos:', data)

            itens = data.get('itens', [])
            form_data = data.get('form', {})

            # Busca instâncias de cliente e vendedor
            cliente_id = form_data.get('cliente')
            vendedor_id = form_data.get('vendedor')

            cliente = Clientes.objects.filter(pk=cliente_id).first()
            vendedor = Vendedores.objects.filter(pk=vendedor_id).first()

            # Calcula o desconto total e o total da venda
            desconto_total = sum(int(item.get('desconto', '0').replace('%', '')) for item in itens)
            

            total_venda = sum(float(item.get('preco', '0').replace(',', '.')) for item in itens)
            print(f'Total venda: {total_venda}')



            # Cria a venda
            venda = Vendas(
                descricao='; '.join([f"{item['codigo_barras']}, {item['descricao']}, {item['tamanho']}, {item['cor']}, {item['quantidade']}" for item in itens]),
                cliente=cliente,
                desconto=desconto_total,
                vendedor=vendedor,
                forma_pagamento=form_data.get('radio'),
                total=total_venda,
            )
            venda.save()

            # Geração do recibo
            print("Iniciando geração do recibo...")
            recibo = {'descricao': [], 'tamanho': [], 'cor': [], 'venda': [], 'quantidade':[]}  # Inicializamos as listas

            for item in itens:
                recibo['descricao'].append(item['descricao'])
                recibo['tamanho'].append(item['tamanho'])
                recibo['cor'].append(item['cor'])
                preco = float(item['preco'].replace(',', '.'))
                recibo['venda'].append(preco)
                recibo['quantidade'].append(item['quantidade'])

            # Convertendo as listas para strings, unindo os valores com ', '
            recibo['descricao'] = ', '.join(recibo['descricao'])
            recibo['tamanho'] = ', '.join(recibo['tamanho'])
            recibo['cor'] = ', '.join(recibo['cor'])
            recibo['venda'] = ', '.join([f"R$ {venda:.2f}" for venda in recibo['venda']])
            recibo['quantidade'] = ', '.join(recibo['quantidade'])
            print(f"Recibo gerado: {recibo}")

            # Serializando mensagem para RabbitMQ
            try:
                print("Serializando mensagem para RabbitMQ...")
                message = json.dumps({
                    "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    "vendedor": vendedor.nome if vendedor else "",
                    "cliente": cliente.nome if cliente else "",
                    "forma_pagamento": form_data.get('radio'),
                    "total": float(total_venda),
                    "recibo": recibo
                }).encode('latin1')
                print(f"Mensagem serializada: {message}")

                # Envio para RabbitMQ
                try:
                    print("Criando RabbitMQPublisher...")
                    publisher = RabbitMQPublisher()
                    print("Publisher criado com sucesso.")
                    publisher.send_message(message)
                    print("Mensagem enviada para RabbitMQ.")
                except Exception as e:
                    print(f"Erro ao enviar mensagem para o RabbitMQ: {e}")

            except Exception as e:
                print(f'Erro ao serializar mensagem: {e}')

            return JsonResponse({'success': True})
        
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Erro ao decodificar JSON. Verifique o formato dos dados enviados.'}) 
            
        except Exception as e:           
            
            return JsonResponse({'success': False, 'error': e})

    return JsonResponse({'success': False, 'error': 'Método não permitido'})


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
    global lista_preco
    template_name = 'vendas/partials/_table.html'
    print('AQUI FOI CHAMADO A FUNÇÃO DELETAR VENDA')
    print(f'essa é a lista fora da session: {lista_preco}')
    lista_preco_session = request.session.get('lista_preco', [])
    print(f'Obtendo a lista_session para deletar: {lista_preco_session}')
    id_str = str(id)
    print(f'Item a ser deletado: {id_str}')
    ocorrencia_excluida_session = False
    lista_preco_session = [item for item in lista_preco_session if not (item['codigo_barras'] == id_str and not ocorrencia_excluida_session and (ocorrencia_excluida_session := True))]
    ocorrencia_excluida = False
    lista_preco = [item for item in lista_preco if not (item['codigo_barras'] == id_str and not ocorrencia_excluida and (ocorrencia_excluida := True))]   
    request.session['lista_preco'] = lista_preco_session
    request.session.modified = True
    print(f'Lista após deletar: {lista_preco}')
    print(f'essa é a session: {request.session.get('lista_preco', [])}')

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