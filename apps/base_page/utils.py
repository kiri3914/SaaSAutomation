from datetime import datetime, date, timedelta
from django.db.models import FloatField

from django.utils import timezone
from django.db.models import Count, Q, Prefetch, F
from django.db.models.functions import Coalesce
from ..mainapp.models import Course
from django.conf import settings
from ..students.models import Student

def get_dashboard_data(branch_id=1, force_refresh=False):
    """Получает данные для дашборда из локальной БД"""
    if branch_id is None:
        branch_id = 1
    try:
        branch_id = int(branch_id)
    except (TypeError, ValueError):
        branch_id = 1

    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Базовый QuerySet для курсов с оптимизированной загрузкой
    base_course_qs = Course.objects.filter(
        branch_id=branch_id,
        is_active=True
    )

    # Получаем все курсы одним запросом и разделяем их в памяти
    all_courses = list(base_course_qs.select_related('branch'))

    # Получаем активные группы
    active_enrollment_groups = list(filter(lambda c: c.date_start >= today, all_courses))
    active_groups = list(filter(lambda c: c.date_start <= today, all_courses))
    groups_next_month = list(filter(lambda c: isinstance(c.next_month, date) and c.next_month <= next_week, all_courses))

    # Оптимизированный QuerySet для студентов с агрегацией
    base_student_qs = Student.objects.filter(
        studies=True,
        course__branch_id=branch_id
    ).select_related('course')

    # Получаем статистику одним запросом
    student_stats = base_student_qs.aggregate(
        active_students_count=Count('id', filter=Q(course__date_start__lte=today)),
        new_students_count=Count('id', filter=Q(create_at__gte=month_ago))
    )

    # Оптимизируем получение должников
    debtors = base_student_qs.filter(
        course__date_start__lte=today
    )
    debtors = [s for s in debtors if s.remainder_for_current_mount > 0]
    debtors_groups = [s.course for s in debtors]
    
    for group in debtors_groups:
        if group not in groups_next_month:
            groups_next_month.append(group)

    no_contract_students = base_student_qs.filter(contract=False)
    last_students = base_student_qs.order_by('-create_at')[:5]

    # Расчет средней заполняемости
    avg_fill_rate = round(
        sum(group.fill_rate for group in active_groups) / len(active_groups)
        if active_groups else 0, 
        1
    )

    students_data = {
        'debtors': debtors,
        'no_contract_students': no_contract_students,
        'last_students': last_students,
        'active_students_count': student_stats['active_students_count'],
        'count_students_last_month': student_stats['new_students_count']
    }

    total_students = base_student_qs.count()



    dashboard_data = {
        'courses': {
            'active_enrollment_groups': active_enrollment_groups,
            'active_groups_fill_rate': active_groups,
            'groups_starting_next_month_within_week': groups_next_month,
            'active_groups_count': len(active_groups)
        },
        'students': students_data,
        'total_stats': {
            'total_students': total_students,
            'total_courses': len(active_groups),
            'avg_fill_rate': avg_fill_rate,
            'upcoming_groups_count': len(active_enrollment_groups)
        }
    }
    return dashboard_data
