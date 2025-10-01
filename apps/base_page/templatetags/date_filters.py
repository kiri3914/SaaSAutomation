from django import template
from datetime import datetime, date
import locale

register = template.Library()

@register.filter
def russian_date(date_value):
    """Преобразует дату в формат '15 января 2025'"""
    if not date_value:
        return ""
    
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    
    try:
        # Если получили строку, преобразуем её в date
        if isinstance(date_value, str):
            date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
        # Если получили datetime, преобразуем в date
        elif isinstance(date_value, datetime):
            date_obj = date_value.date()
        # Если уже получили date, используем как есть
        elif isinstance(date_value, date):
            date_obj = date_value
        else:
            return str(date_value)

        return f"{date_obj.day} {months[date_obj.month]} {date_obj.year}"
    except (ValueError, AttributeError):
        return str(date_value)

@register.filter
def count_active_students(students):
    """Подсчитывает количество активных студентов"""
    return sum(1 for student in students if student.studies)

@register.filter
def format_price(value):
    """Форматирует цену с разделителями тысяч"""
    if not value:
        return "0"
    try:
        # Разделяем число на целую и дробную части
        parts = str(value).split('.')
        # Форматируем целую часть с разделителями
        integer_part = '{:,}'.format(int(parts[0])).replace(',', ' ')
        # Если есть дробная часть, добавляем её
        if len(parts) > 1:
            return f"{integer_part}.{parts[1]}"
        return integer_part
    except (ValueError, TypeError):
        return value 