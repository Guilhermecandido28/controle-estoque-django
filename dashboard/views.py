from django.shortcuts import render
from django.http import JsonResponse
from .utils import Context, Graficos
from .forms import SaidaForms
from .models import Saidas


def dashboard(request):
    template_name = 'dashboard/dashboard.html'
    context = Context.contexto()
    return render(request, template_name , context)

def salvar_saida(request):
    form = SaidaForms(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            obj = Saidas.objects.last()
            return render(request, 'dashboard/partials/_linha_tabela.html', {'saida': obj})
        else:
            # Se o formulário não for válido, retorne uma resposta JSON com os erros
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)


def card1_entradas(request):
    template_name = 'dashboard/partials/card1/_card1_entradas.html'
    context = {
        'vendas_dia': Context.contexto()['vendas_dia'],
        'vendas_ontem': Context.contexto()['vendas_ontem']
        }
    return render(request, template_name, context )

def card1_saidas(request):    
    template_name = 'dashboard/partials/card1/_card1_saidas.html'
    context = {
        'saidas_dia': Context.contexto()['saidas_dia'],
        'saidas_ontem': Context.contexto()['saidas_ontem']
        }
    return render(request, template_name, context )
    
def card2_entradas(request):
    template_name = 'dashboard/partials/card2/_card2_entradas.html'
    context = {
        'vendas_ano': Context.contexto()['vendas_ano'],
        'vendas_ano_passado': Context.contexto()['vendas_ano_passado']
        }
    return render(request, template_name, context)

def card2_saidas(request):    
    template_name = 'dashboard/partials/card2/_card2_saidas.html'
    context = {
        'saidas_ano': Context.contexto()['saidas_ano'],
        'saidas_ano_passado': Context.contexto()['saidas_ano_passado']
        }
    return render(request, template_name, context)
    
def card3_entradas(request):
    template_name = 'dashboard/partials/card3/_card3_entradas.html'
    context = {
        'vendas_mes': Context.contexto()['vendas_mes'],
        'vendas_mes_passado': Context.contexto()['vendas_mes_passado']
        }
    return render(request, template_name, context)

def card3_saidas(request):    
    template_name = 'dashboard/partials/card3/_card3_saidas.html'
    context = {
        'saidas_mes': Context.contexto()['saidas_mes'],
        'saidas_mes_passado': Context.contexto()['saidas_mes_passado']
        }
    return render(request, template_name, context)
    

def card4_saidas(request):    
    return render(request, 'dashboard/partials/card4/_card4_saidas.html')
    
def card4_entradas(request):
    return render(request, 'dashboard/partials/card4/_card4_entradas.html')

def card5_saidas(request):    
    return render(request, 'dashboard/partials/card5/_card5_saidas.html')
    
def card5_entradas(request):
    template_name = 'dashboard/partials/card3/_card5_entradas.html'
    context = {
        'vendas_mes': Context.contexto()['vendas_mes'],
        'vendas_mes_passado': Context.contexto()['vendas_mes_passado']
        }
    return render(request, template_name, context)




