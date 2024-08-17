from django import template
import locale
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplica um número por uma quantidade."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value  # Retorna o valor original se ocorrer um erro
    
@register.filter(name='apply_discount')
def apply_discount(total, discount):
    """Aplica um desconto ao total."""
    try:
        discount_value = float(discount) / 100
        total_with_discount = total - (total * discount_value)
        return total_with_discount
    except (ValueError, TypeError):
        return total  # Retorna o valor original se ocorrer um erro

@register.filter(name='currency')
def currency(value):
    if value in (None, '', 'NaN'):
        return 'R$ 0,00'

    try:
        # Convertendo o valor para float se necessário
        value = float(value) if isinstance(value, (str, Decimal)) else value
        
        # Formatando o valor para 2 casas decimais e adicionando separadores de milhar
        formatted_value = f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        # Retornando o valor formatado com o símbolo da moeda
        return f'R$ {formatted_value}'
    except (ValueError, TypeError) as e:
        print(f"Erro ao converter valor: {e}")
        return f'Erro: {e}'
    
@register.filter(name='forma_pagamento')
def forma_pagamento(string):
    if string == 'CARTAO':
        return 'Cartão de Crédito'
    elif string == 'DEBITO':
        return 'Cartão de Débito'
    elif string == 'PIX':
        return 'PIX'
    else:
        return 'Dinheiro'
    

@register.filter(name='venda')
def vis_venda(string):
    
    sem_parenteses = string.strip('()')
    
    elementos = sem_parenteses.split(',')
    elementos_sem_aspas = [elemento.strip().strip("'") for elemento in elementos]
        
    output = ""    
    output += f"{elementos_sem_aspas[1]}, {elementos_sem_aspas[2]}, {elementos_sem_aspas[3].replace("'",'').replace(')','')} \n"    
    output += f", {elementos_sem_aspas[0]}. \n"    
    return output





