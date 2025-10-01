from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.core.exceptions import PermissionDenied

from apps.mainapp.models import Course

from .models import CustomUser
from .serializers import CustomUserSerializer
from ..utils.base_views import BaseQuerysetView


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверный номер телефона или пароль.')
  
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')    


class UserViewSet(BaseQuerysetView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch__id']

    related_name_filter = 'branch'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super().get_queryset()
            if not self.request.user.branch:
                return CustomUser.objects.none()
            return CustomUser.objects.filter(Q(**self.get_filter_kwargs()) | Q(is_superuser=True))
        return self.queryset.model.objects.none()


class RecruiterDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/recruiter_detail.html'
    context_object_name = 'recruiter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recruiter = self.object
        
        # Проверка доступа
        if not (self.request.user.is_superuser or 
                (self.request.user.is_branch_admin and 
                 self.request.user.branch == recruiter.branch)):
            raise PermissionDenied
            
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        # Все студенты рекрутера
        all_students = recruiter.recruited_students.all()
        
        # Статистика по студентам
        context['student_stats'] = {
            'total_students': all_students.count(),
            'active_students': all_students.filter(studies=True).count(),
            'inactive_students': all_students.filter(studies=False).count(),
            'this_month_students': all_students.filter(
                create_at__month=current_month,
                create_at__year=current_year
            ).count(),
        }

        # Финансовая статистика
        all_payments = sum([student.full_payment for student in all_students])
        this_month_payments = sum([
            student.full_payment for student in all_students.filter(
                create_at__month=current_month,
                create_at__year=current_year
            )
        ])
        commission = all_payments * 0.03  # 3% комиссия
        this_month_commission = this_month_payments * 0.03  # 3% комиссия за текущий месяц

        context['financial_stats'] = {
            'total_payments': all_payments,
            'total_commission': commission,
            'this_month_commission': this_month_commission,
            'avg_payment_per_student': all_payments / all_students.count() if all_students.count() > 0 else 0,
            'this_month_payments': this_month_payments,
        }

        # Статистика по месяцам
        monthly_stats = []
        students_by_month = all_students.annotate(
            month=TruncMonth('create_at')
        ).values('month').annotate(
            students_count=Count('id')
        ).order_by('-month')[:12]

        for month_stat in students_by_month:
            month_students = all_students.filter(create_at__month=month_stat['month'].month,
                                               create_at__year=month_stat['month'].year)
            total_payments = sum(student.full_payment for student in month_students)
            monthly_stats.append({
                'month': month_stat['month'],
                'students_count': month_stat['students_count'],
                'total_payments': total_payments
            })

        context['monthly_stats'] = monthly_stats

        # Статистика по направлениям
        direction_stats = {}
        for student in all_students:
            direction = student.course.direction.title
            if direction not in direction_stats:
                direction_stats[direction] = {
                    'students_count': 0,
                    'total_payments': 0
                }
            direction_stats[direction]['students_count'] += 1
            direction_stats[direction]['total_payments'] += student.full_payment

        direction_stats = [
            {
                'course__direction__title': direction,
                'students_count': stats['students_count'],
                'total_payments': stats['total_payments']
            }
            for direction, stats in direction_stats.items()
        ]
        direction_stats.sort(key=lambda x: x['students_count'], reverse=True)

        context['direction_stats'] = direction_stats

        # Конверсия
        context['conversion_stats'] = {
            'total': int((all_students.filter(studies=True).count() / all_students.count() * 100) if all_students.count() > 0 else 0),
            'this_month': int((
                all_students.filter(
                    studies=True,
                    create_at__month=current_month,
                    create_at__year=current_year
                ).count() / 
                all_students.filter(
                    create_at__month=current_month,
                    create_at__year=current_year
                ).count() * 100
            ) if all_students.filter(create_at__month=current_month).count() > 0 else 0),
        }

        # Добавим данные по активным группам
        active_groups = []
        for course in Course.objects.filter(student_course__recruiter=recruiter).distinct():
            students = course.student_course.filter(
                recruiter=recruiter,
                studies=True
            )
            if students.exists():
                total_payments = sum(student.full_payment for student in students)
                active_groups.append({
                    'title': course.title,
                    'students_count': students.count(),
                    'commission': total_payments * 0.03  # 3% комиссия
                })

        context['active_groups'] = sorted(active_groups, key=lambda x: x['students_count'], reverse=True)

        return context


