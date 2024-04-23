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
    return locale.currency(value)

