from django import template
import locale
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies a number by a given quantity."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        pass  # Not numeric, so just return the original value

@register.filter(name='currency')
def currency(value):
    
    if value in (None, '', 'NaN'):
        return 'N/A'
    try:
        value = float(value) if isinstance(value, (str, Decimal)) else value
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError, InvalidOperation) as e:
        print(f"Erro ao converter valor: {e}")
        return 'N/A'
    
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
