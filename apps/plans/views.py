from django.shortcuts import render
from django.db import models
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CoursePlanner
from django.template.defaulttags import register
from apps.branches.models import Branch, Direction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from collections import defaultdict
import xlsxwriter
from io import BytesIO
import pandas as pd
from django.conf import settings
from datetime import datetime, timedelta
from apps.mainapp.models import Course
from django.db.models import Count

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class PlanningView(LoginRequiredMixin, TemplateView):
    template_name = 'plans/planning.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MAX_GROUP_SIZE'] = settings.MAX_GROUP_SIZE
        branch_id = self.request.GET.get('branch_id')
        direction_id = self.request.GET.get('direction')
        
        # Если branch_id не указан, используем branch_id пользователя или первый филиал
        if not branch_id:
            branch_id = self.request.user.branch_id if self.request.user.branch_id else Branch.objects.first().id
        else:
            branch_id = int(branch_id)
            
        # Преобразуем direction_id в целое число, если он есть
        if direction_id:
            try:
                direction_id = int(direction_id)
            except ValueError:
                direction_id = None
        
        # Получаем списки из сессии для конкретного филиала
        session_key = f'hidden_courses_{branch_id}'
        hidden_courses = self.request.session.get(session_key, [])
        
        planner = CoursePlanner(branch_id=branch_id)
        schedule = planner.calculate_next_starts()
        
        # Получаем все курсы
        all_courses = schedule.index.tolist()
        
        # Фильтруем по направлению если выбрано
        if direction_id:
            direction = Direction.objects.get(id=direction_id)
            all_courses = [course for course in all_courses if direction.title in course]
        
        # Фильтруем скрытые курсы
        visible_courses = [course for course in all_courses if course not in hidden_courses]
        filtered_schedule = schedule.loc[visible_courses] if visible_courses else schedule
        
        # Добавляем статистику по месяцам только для видимых курсов
        monthly_stats = defaultdict(lambda: {'count': 0})
        if context.get('show_hidden'):
            courses_for_stats = all_courses
        else:
            courses_for_stats = visible_courses
        
        for course in courses_for_stats:
            for month in schedule.columns:
                if schedule.loc[course, month]:
                    monthly_stats[month]['count'] += 1
        
        context.update({
            'schedule': filtered_schedule.to_dict(),
            'courses': visible_courses,
            'months': schedule.columns.tolist(),
            'selected_branch_id': branch_id,
            'branches': Branch.objects.all(),
            'directions': Direction.objects.all(),
            'selected_direction': direction_id,
            'hidden_courses': hidden_courses,
            'show_hidden': self.request.GET.get('show_hidden', False),
            'monthly_stats': {k: v for k, v in monthly_stats.items() if v['count'] > 0}
        })
        
        if context['show_hidden']:
            context['courses'] = all_courses
            context['schedule'] = schedule.to_dict()
        
        # Получаем активные наборы
        active_recruitments = Course.objects.filter(
            branch_id=branch_id,
            is_active=True,
            date_start__gt=datetime.now().date()
        ).annotate(
            student_count=Count('student_course', filter=models.Q(student_course__studies=True))
        ).order_by('date_start')

        # Рассчитываем план набора для каждого курса
        recruitment_plans = []
        for course in active_recruitments:
            weeks_until_start = (course.date_start - datetime.now().date()).days // 7
            if weeks_until_start <= settings.WEEKS_BEFORE_START:
                students_needed = settings.MAX_GROUP_SIZE - course.student_count
                if students_needed > 0:
                    weekly_goal = max(1, students_needed // (weeks_until_start if weeks_until_start > 0 else 1))
                    
                    # Создаем план по неделям
                    weeks_breakdown = []
                    current_target = course.student_count
                    for i in range(weeks_until_start):
                        current_target = min(
                            settings.MAX_GROUP_SIZE,
                            course.student_count + (weekly_goal * (i + 1))
                        )
                        weeks_breakdown.append({
                            'week': i + 1,
                            'target': current_target
                        })
                    
                    # Правильный расчет процента заполненности
                    progress_percentage = int((course.student_count * 100) / settings.MAX_GROUP_SIZE)  # Округляем до целого числа
                    
                    recruitment_plans.append({
                        'course': course,
                        'weeks_left': weeks_until_start,
                        'current_students': course.student_count,
                        'students_needed': students_needed,
                        'weekly_goal': weekly_goal,
                        'progress_percentage': progress_percentage,  # Теперь это целое число
                        'weeks_breakdown': weeks_breakdown
                    })

        context['recruitment_plans'] = recruitment_plans
        return context

@require_POST
def toggle_course_visibility(request):
    course_name = request.POST.get('course_name')
    branch_id = request.POST.get('branch_id')
    
    if not course_name or not branch_id:
        return JsonResponse({'status': 'error', 'message': 'Course name and branch_id are required'})
    
    # Используем уникальный ключ для каждого филиала
    session_key = f'hidden_courses_{branch_id}'
    hidden_courses = request.session.get(session_key, [])
    
    if course_name in hidden_courses:
        hidden_courses.remove(course_name)
    else:
        hidden_courses.append(course_name)
    
    request.session[session_key] = hidden_courses
    request.session.modified = True
    
    return JsonResponse({'status': 'success'})

@require_POST
def update_courses_order(request):
    new_order = request.POST.getlist('courses[]')
    if not new_order:
        return JsonResponse({'status': 'error', 'message': 'New order is required'})
    
    request.session['courses_order'] = new_order
    request.session.modified = True
    
    return JsonResponse({'status': 'success'})

def export_planning(request):
    branch_id = request.GET.get('branch_id')
    if not branch_id:
        branch_id = request.user.branch_id if request.user.branch_id else Branch.objects.first().id
    
    # Получаем скрытые курсы для филиала
    session_key = f'hidden_courses_{branch_id}'
    hidden_courses = request.session.get(session_key, [])
    
    # Получаем данные планирования
    planner = CoursePlanner(branch_id=branch_id)
    schedule = planner.calculate_next_starts()
    
    # Фильтруем скрытые курсы
    all_courses = schedule.index.tolist()
    visible_courses = [course for course in all_courses if course not in hidden_courses]
    filtered_schedule = schedule.loc[visible_courses] if visible_courses else schedule
    
    # Создаем Excel файл
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    # Добавляем стили
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#f3f4f6',
        'border': 1
    })
    cell_format = workbook.add_format({
        'border': 1
    })
    date_format = workbook.add_format({
        'border': 1,
        'bg_color': '#e5e7eb'
    })
    
    # Записываем заголовки
    worksheet.write(0, 0, 'Курс', header_format)
    for col, month in enumerate(filtered_schedule.columns, 1):
        worksheet.write(0, col, month, header_format)
    
    # Записываем данные
    for row, course in enumerate(filtered_schedule.index, 1):
        worksheet.write(row, 0, course, cell_format)
        for col, month in enumerate(filtered_schedule.columns, 1):
            value = filtered_schedule.loc[course, month]
            if pd.notna(value):  # Проверяем, что значение не NaN
                worksheet.write(row, col, value, date_format)
            else:
                worksheet.write(row, col, '', cell_format)
    
    # Устанавливаем ширину столбцов
    worksheet.set_column(0, 0, 30)  # Для названия курса
    worksheet.set_column(1, len(filtered_schedule.columns), 15)  # Для дат
    
    workbook.close()
    output.seek(0)
    
    # Формируем имя файла с датой
    from datetime import datetime
    filename = f'planning_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
