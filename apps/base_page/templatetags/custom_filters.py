from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_payment_date(value):
    """
    Форматирует дату платежа
    """
    if not value:
        return ''
    try:
        # Если дата приходит в формате ISO
        date_obj = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return date_obj.strftime('%d.%m.%Y')
    except (ValueError, AttributeError):
        try:
            # Если дата приходит в другом формате
            date_obj = datetime.strptime(str(value), '%Y-%m-%d')
            return date_obj.strftime('%d.%m.%Y')
        except (ValueError, TypeError):
            return value 
        
@register.filter
def percentage(value, total):
    try:
        return int((value * 100) / total) if total > 0 else 0
    except (ValueError, ZeroDivisionError, TypeError):
        return 0