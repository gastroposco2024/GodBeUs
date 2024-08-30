from django import template
import locale

register = template.Library()

@register.filter
def format_number(value):
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
    return locale.format_string("%d", value, grouping=True)

@register.filter
def remove_decimals_and_dots(value):
    try:
        # Asegúrate de que el valor sea un número
        number = float(value)
        
        # Redondea el número al entero más cercano
        rounded_number = round(number)
        
        # Convierte el número a entero y lo convierte a string
        integer_string = str(int(rounded_number))
        
        return integer_string
    except (ValueError, TypeError):
        # Devuelve el valor original si no se puede convertir a número
        return value

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def add(value, arg):
    """Suma dos valores."""
    return value + arg