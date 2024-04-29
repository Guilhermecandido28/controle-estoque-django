from django.shortcuts import render, redirect
from .filters import CodBarrasFilter
from estoque.models import Estoque
from .models import Vendas
from clientes.models import Clientes
from .forms import VendaForms
from datetime import datetime

lista_preco = []

def venda(request):
    form = VendaForms()
    object = Estoque.objects.select_related('descricao').all()
    object_filter = CodBarrasFilter(request.GET, queryset=object)    
    context = {'filter': object_filter, 'form':form}
    return render(request, 'vendas/venda.html', context)


def inserir_venda(request): 
    if request.method == 'POST':
        # Obter os dados do formulário de pesquisa
        filtro = CodBarrasFilter(request.POST, queryset=Estoque.objects.all())       
        # Aplicar o filtro
        obj = filtro.qs.values('codigo_barras', 'descricao', 'tamanho', 'cor', 'venda')               
        quantidade = request.POST.get('quantidade', None)
        if obj.exists():
            for item in obj:               
                total = int(quantidade) * item['venda']  # Calcula o total
                item['total'] = total  # Adiciona o total ao dicionário do item
                lista_preco.append(item)

        
        print(lista_preco)
                    
    template_name = 'vendas/partials/_table.html'    
    context = {'object': obj, 'filtro': filtro, 'quantidade':quantidade}        
    return render(request, template_name, context)

def salvar_venda(request):    
    if request.method == 'POST':
        print("Dados do formulário POST recebidos:", request.POST)
        
        valores = [(item['codigo_barras'], item['descricao'], item['tamanho'], item['cor']) for item in lista_preco]
        descricao = ', '.join(map(str, valores))
        
        cliente_id = request.POST.get('cliente')
        cliente = Clientes.objects.get(pk=cliente_id)
        print("Cliente:", cliente)
        
        desconto = request.POST.get('desconto')
        print("Desconto:", desconto)
        
        forma_pagamento = request.POST.get('radio')
        print("Forma de pagamento:", forma_pagamento)
        
        data = datetime.now()
        total = sum(item['total'] for item in lista_preco)
        
        # Agora, vamos verificar se lista_preco tem os dados esperados
        print("Dados de lista_preco:", lista_preco)
        
        # Agora, vamos verificar se a soma está correta
        print("Total calculado:", total)
        
        # Agora, vamos verificar se estamos criando o objeto Vendas corretamente
        print("Descrição:", descricao)
        print("Data:", data)
        
        # Agora, vamos tentar criar o objeto Vendas e verificar se há erros
        try:
            Vendas.objects.create(descricao=descricao, cliente=cliente, desconto=desconto, forma_pagamento=forma_pagamento, data=data, total=total)
            print('Venda salva com sucesso')
            lista_preco.clear()
            print(lista_preco)
            return redirect('vendas')
        except Exception as e:
            print('Erro ao salvar venda:', e)
            # Redireciona para a página anterior (com mensagem de erro)
            return redirect('vendas.html')

                  

            
   
               




    

