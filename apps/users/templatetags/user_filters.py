from django import template
from django.template.defaultfilters import floatformat
import locale

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0 

@register.filter
def intcomma(value):
    """Converts an integer to a string containing commas every three digits"""
    try:
        if isinstance(value, str):
            value = float(value)
        # Форматируем число с разделителями групп разрядов
        formatted = "{:,.0f}".format(float(value))
        # Заменяем запятые на пробелы для лучшей читаемости
        return formatted.replace(',', ' ')
    except (ValueError, TypeError):
        return value 