from django import template
import locale

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
    return locale.currency(float(value))

@register.filter(name='venda')
def vis_venda(string):
    print(string)
    sem_parenteses = string.strip('()')
    
    elementos = sem_parenteses.split(',')
    elementos_sem_aspas = [elemento.strip().strip("'") for elemento in elementos]
        
    output = ""    
    output += f"{elementos_sem_aspas[1]}, {elementos_sem_aspas[2]}, {elementos_sem_aspas[3].replace("'",'').replace(')','')} \n"    
    output += f", {elementos_sem_aspas[0]}. \n"    
    return output
