from django.utils import timezone
from vendas.models import Vendas
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth, ExtractWeekDay
from django.http import JsonResponse
from datetime import datetime, timedelta
from .forms import SaidaForms
from .models import Saidas

class Datas:
    @staticmethod
    def datas():
        hoje = timezone.now().date()
        ontem = hoje - timezone.timedelta(days=1)
        mes = hoje.month
        mes_passado = hoje.month-1
        ano = hoje.year
        ano_passado = hoje.year-1


        return {
            'hoje': hoje,
            'ontem': ontem,
            'mes': mes,
            'ano': ano,
            'mes_passado': mes_passado,
            'ano_passado': ano_passado
        }

class CalculoVendas:
    def __init__(self) -> None:
        self.data = Datas.datas()

    def vendas_dia(self):

        return Vendas.objects.filter(data=self.data['hoje']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def saidas_dia(self):
        return Saidas.objects.filter(data=self.data['hoje']).aggregate(soma=Sum('valor'))['soma'] or 0
    
    def saidas_ontem(self):
        return Saidas.objects.filter(data=self.data['ontem']).aggregate(soma=Sum('valor'))['soma'] or 0
    
    def vendas_ontem(self):
        return Vendas.objects.filter(data=self.data['ontem']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def vendas_mes(self):
        return Vendas.objects.filter(data__month=self.data['mes']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def saidas_mes(self):
        return Saidas.objects.filter(data__month=self.data['mes']).aggregate(soma=Sum('valor'))['soma'] or 0
    
    def vendas_mes_passado(self):
        return Vendas.objects.filter(data__month=self.data['mes_passado']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def saidas_mes_passado(self):
        return Saidas.objects.filter(data__month=self.data['mes_passado']).aggregate(soma=Sum('valor'))['soma'] or 0
    
    def vendas_ano(self):
        return Vendas.objects.filter(data__year=self.data['ano']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def saidas_ano(self):
        return Saidas.objects.filter(data__year=self.data['ano']).aggregate(soma=Sum('valor'))['soma'] or 0
    
    def vendas_ano_passado(self):        
        return Vendas.objects.filter(data__year=self.data['ano_passado']).aggregate(soma=Sum('total'))['soma'] or 0
    
    def saidas_ano_passado(self):        
        return Saidas.objects.filter(data__year=self.data['ano_passado']).aggregate(soma=Sum('valor'))['soma'] or 0
    
class Graficos:
    def vendasxmes(self):  
        dados = Vendas.objects.annotate(mes=ExtractMonth('data')).values('mes').annotate(total_vendas=Sum('total')).order_by('mes')
        saidas = Saidas.objects.annotate(mes=ExtractMonth('data')).values('mes').annotate(total_vendas=Sum('valor')).order_by('mes')
        
        # Criar um dicionário com os dados formatados para JSON
        json_data = {
            'entradas': {item['mes']: float(item['total_vendas']) for item in dados},
            'saidas': {item['mes']: float(item['total_vendas']) for item in saidas}
        }

        # Retorna o JSON serializado
        return JsonResponse(json_data)
    

    def vendasxdia(self):
        # Data atual
        hoje = datetime.now().date()

        # Data de início da semana atual (segunda-feira)
        inicio_semana_atual = hoje - timedelta(days=hoje.weekday())
        fim_semana_atual = inicio_semana_atual + timedelta(days=6)

        # Data de início da semana passada (segunda-feira)
        inicio_semana_passada = inicio_semana_atual - timedelta(days=7)
        fim_semana_passada = inicio_semana_passada + timedelta(days=6)

        # Obter dados da semana atual
        dados_semana_atual = Vendas.objects.filter(data__range=[inicio_semana_atual, fim_semana_atual]) \
            .annotate(dia=ExtractWeekDay('data')).values('dia') \
            .annotate(total_vendas=Sum('total')).order_by('dia')

        # Obter dados da semana passada
        dados_semana_passada = Vendas.objects.filter(data__range=[inicio_semana_passada, fim_semana_passada]) \
            .annotate(dia=ExtractWeekDay('data')).values('dia') \
            .annotate(total_vendas=Sum('total')).order_by('dia')
        
        saidas = Saidas.objects.annotate(dia=ExtractWeekDay('data')).values('dia').annotate(total_vendas=Sum('valor')).order_by('dia')

        # Criar um dicionário com os dados formatados para JSON
        json_data = {
            'semana_atual': {item['dia']: float(item['total_vendas']) for item in dados_semana_atual},
            'semana_passada': {item['dia']: float(item['total_vendas']) for item in dados_semana_passada},
            'saidas': {item['dia']: float(item['total_vendas']) for item in saidas}
        }

        # Retorna o JSON serializado
        return JsonResponse(json_data)
    
    def vendasxfp_mes(self):
        # Obtém o mês atual
        mes_atual = datetime.now().month

        # Anotação para calcular o total de vendas por forma de pagamento no mês atual
        dados = Vendas.objects.filter(data__month=mes_atual).annotate(
            forma_pagamento_annotated=F('forma_pagamento')
        ).values('forma_pagamento_annotated').annotate(
            total_vendas=Sum('total')
        ).order_by('forma_pagamento_annotated')

        # Criar um dicionário com os dados formatados para JSON
        json_data = {}
        for item in dados:
            forma_pagamento = item['forma_pagamento_annotated']
            total_vendas = float(item['total_vendas'])

            json_data[forma_pagamento] = total_vendas
        print(json_data)
        # Retorna o JSON serializado
        return JsonResponse(json_data)
    
    def vendasxfp_dia(self):
        # Obtém o mês atual
        dia = datetime.now()

        # Anotação para calcular o total de vendas por forma de pagamento no mês atual
        dados = Vendas.objects.filter(data=dia).annotate(
            forma_pagamento_annotated=F('forma_pagamento')
        ).values('forma_pagamento_annotated').annotate(
            total_vendas=Sum('total')
        ).order_by('forma_pagamento_annotated')

        # Criar um dicionário com os dados formatados para JSON
        json_data = {}
        for item in dados:
            forma_pagamento = item['forma_pagamento_annotated']
            total_vendas = float(item['total_vendas'])

            json_data[forma_pagamento] = total_vendas
        # Retorna o JSON serializado
        return JsonResponse(json_data)

class Context:

    @staticmethod
    def contexto():
        calculo = CalculoVendas()        
        return {
            'vendas_dia': calculo.vendas_dia(),
            'saidas_dia': calculo.saidas_dia(),
            'saidas_ontem': calculo.saidas_ontem(),
            'vendas_ontem': calculo.vendas_ontem(),
            'vendas_mes': calculo.vendas_mes(),
            'saidas_mes': calculo.saidas_mes(),
            'vendas_mes_passado': calculo.vendas_mes_passado(),
            'saidas_mes_passado': calculo.saidas_mes_passado(),
            'vendas_ano': calculo.vendas_ano(),
            'saidas_ano': calculo.saidas_ano(),
            'vendas_ano_passado': calculo.vendas_ano_passado(),
            'saidas_ano_passado': calculo.saidas_ano_passado(),
            'forms': SaidaForms(),
            'saidas': Saidas.objects.all()                  
        }