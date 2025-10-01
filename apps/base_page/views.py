from datetime import datetime, timedelta, date
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from rest_framework import status
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from .utils import get_dashboard_data

from .serializers import (
    GetCourseBasePageSerializer,
    ActiveGroupsFillRateSerializer,
    GetStudentsBasePageSerializer,
    GetGroupsStartingNextMonthWithinWeekSerializer,
    GetDebtorStudentsBasePageSerializer,
)

from ..mainapp.models import Course
from ..sales.models import Client
from ..students.models import Student, PaymentStudent
from ..branches.models import Branch

class BasePageView(APIView):
    manual_parameters = [
        openapi.Parameter(
            'branch_id',
            openapi.IN_QUERY,
            description="ID of the branch to filter",
            type=openapi.TYPE_INTEGER
        )
    ]

    @swagger_auto_schema(manual_parameters=manual_parameters)
    def get_branch_id(self, request):
        branch_id = request.query_params.get('branch_id')
        if not branch_id and request.user.is_superuser:
            return None, Response({'error': 'Branch ID is required when requested by the admin!'}, status=400)
        elif not request.user.is_superuser and branch_id != request.user.branch_id:
            return None, Response({'error': 'You can only view data for your branch!'}, status=403)
        elif not request.user.is_superuser:
            branch_id = request.user.branch_id
        return branch_id, None


class CoursesBasePageView(BasePageView):
    manual_parameters = BasePageView.manual_parameters 

    @swagger_auto_schema(manual_parameters=manual_parameters)
    def get(self, request):
        """
        Это метод для получения данных для главной страницы курсов.
        parameters:
            - name: branch_id
              required: false
              type: integer
              description: ID of the branch to filter
            - name: date_start
              required: false
              type: date
              description: Start date to filter
        responses data:
            - active_enrollment_groups (list): Список активных групп
            - active_groups_fill_rate (list): Список активных групп и их заполненность
            - groups_starting_next_month_within_week (list): Список групп, у которых слудующий месяц начинается в течение недели
            - upcoming_groups (list): Список групп, которые начнутся в будущем
        """


        today = timezone.now().date()
        branch_id, error_response = self.get_branch_id(request)
        if error_response:
            return error_response

        # active enrollment groups
        active_enrollment_groups = self.get_active_enrollment_groups(branch_id=branch_id, today=today)
        
        # active groups fill rate
        active_groups_fill_rate = self.get_active_groups_fill_rate(branch_id=branch_id)
        
        # groups starting next month within a week
        groups_starting_next_month_within_week = self.get_groups_starting_next_month_within_week(branch_id=branch_id, today=today)
        
        # upcoming groups
        upcoming_groups = self.get_upcoming_groups(branch_id=branch_id, today=today)

        # active groups count
        active_groups_count = Course.objects.filter(
            is_active=True,
            branch_id=branch_id,
            date_start__lte=today
        ).count()

        data = {
            'active_enrollment_groups': active_enrollment_groups,
            'active_groups_fill_rate': active_groups_fill_rate,
            'groups_starting_next_month_within_week': groups_starting_next_month_within_week,
            'upcoming_groups': upcoming_groups,
            'active_groups_count': active_groups_count
        }

        return Response(data)
    
    def get_active_groups_fill_rate(self, branch_id):
        """
        active groups fill rate
        """
        active_groups_fill_rate = Course.objects.filter(
            is_active=True,
            branch_id=branch_id)
        active_groups_fill_rate_serialized = ActiveGroupsFillRateSerializer(active_groups_fill_rate, many=True).data
        return active_groups_fill_rate_serialized
    
    def get_active_enrollment_groups(self, branch_id, today):
        """
        active enrollment groups
        """
        active_enrollment_groups = Course.objects.filter(
            date_start__gte=today, 
            is_active=True,
            branch_id=branch_id)
        active_enrollment_groups_serialized = GetCourseBasePageSerializer(active_enrollment_groups, many=True).data
        return active_enrollment_groups_serialized
    
    def get_groups_starting_next_month_within_week(self, branch_id, today):
        next_week = today + timedelta(days=7)
        groups_starting_next_month_within_week = Course.objects.filter(
            is_active=True,
            branch_id=branch_id
        ).order_by('-date_start')
        groups_starting_next_month_within_week = [course 
                                                  for course in groups_starting_next_month_within_week 
                                                    if isinstance(course.next_month, date) 
                                                        and course.next_month <= next_week]  
        groups_starting_next_month_within_week_serialized = GetGroupsStartingNextMonthWithinWeekSerializer(groups_starting_next_month_within_week, many=True).data
        return groups_starting_next_month_within_week_serialized

    def get_upcoming_groups(self, branch_id, today):
        """
        Группы начинающиеся в будущем
        """
        upcoming_groups = Course.objects.filter(
            date_start__gt=today,
            is_active=True,
            branch_id=branch_id
        ).order_by('date_start')
        upcoming_groups_serialized = GetCourseBasePageSerializer(
            upcoming_groups, many=True
        ).data
        return upcoming_groups_serialized

class StudentsBasePageView(BasePageView):
    manual_parameters = BasePageView.manual_parameters 

    @swagger_auto_schema(manual_parameters=manual_parameters)
    def get(self, request):
        today = timezone.now().date()
        branch_id, error_response = self.get_branch_id(request)
        if error_response:
            return error_response 
        
        # debtors
        debtors = self.get_debtors(branch_id, today)   

        # get future students   
        future_students = self.get_future_students(branch_id, today)

        # get last 5 students
        last_students = self.get_last_students(branch_id)
        
        # get count students last month
        count_students_last_month = self.get_count_students_last_month(branch_id, today)
        
        # count active groups and students
        active_students_count = Student.objects.filter(
            studies=True,
            course__branch_id=branch_id,
            course__date_start__lte=today
        ).count()

        data = {
            'debtors': debtors,
            'future_students': future_students,
            'last_students': last_students, 
            'active_students_count': active_students_count,
            'count_students_last_month': count_students_last_month        
        }
        return Response(data, status=status.HTTP_200_OK)

    def get_debtors(self, branch_id, today):
        """
        Студенты, которые учатся, но еще не оплатили: Найти студентов, чьи курсы начались, но оплата не поступила. 
        """
        debtors = Student.objects.filter(
            studies=True,
            course__branch_id=branch_id,
            course__date_start__lte=today
        )
        debtors = [student for student in debtors if student.remainder_for_current_mount > 0]
        debtors_serialized = GetDebtorStudentsBasePageSerializer(debtors, many=True).data
        return debtors_serialized
    
    def get_future_students(self, branch_id, today):
        """
        Студенты, которые активны, но их курс еще не начался: 
        Найти студентов, у которых статус "активный", но дата начала курса еще не наступила. 
        """

        students = Student.objects.filter(
            studies=True,
            course__branch_id=branch_id,
            course__date_start__gt=today
        )
        students_serialized = GetStudentsBasePageSerializer(students, many=True).data
        return students_serialized

    def get_last_students(self, branch_id):
        # last 5 students
        last_students = Student.objects.filter(
            studies=True,
            course__branch_id=branch_id
        ).order_by('-create_at')[:5]
        last_students_serialized = GetStudentsBasePageSerializer(
            last_students, many=True
        ).data
        return last_students_serialized

    def get_count_students_last_month(self, branch_id, today):
        """
        Количество новых студентов за последний месяц
        """
        count_students_last_month = Student.objects.filter(
            create_at__gte=today - timedelta(days=30),
            course__branch_id=branch_id,
            studies=True
        ).count()
        return count_students_last_month

class DashboardView(UserPassesTestMixin, APIView):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_admin or self.request.user.is_branch_admin)
        
    def get(self, request):
        branch_id = request.GET.get('branch_id')
        try:
            # Если пользователь branch_admin, показываем только его филиал
            if request.user.is_branch_admin:
                branch_id = request.user.branch.id
            # Для обычных админов
            elif branch_id:
                branch_id = int(branch_id)
            elif request.user.branch:
                branch_id = request.user.branch.id
            else:
                first_branch = Branch.objects.first()
                branch_id = first_branch.id if first_branch else None
        except (ValueError, TypeError, Branch.DoesNotExist):
            first_branch = Branch.objects.first()
            branch_id = first_branch.id if first_branch else None

        force_refresh = request.GET.get('refresh') == 'true'
        dashboard_data = get_dashboard_data(branch_id, force_refresh)
        
        context = {
            # Если branch_admin, показываем только его филиал в селекторе
            'branches': [request.user.branch] if request.user.is_branch_admin else Branch.objects.filter(is_active=True),
            'selected_branch_id': branch_id,
            'total_stats': dashboard_data.get('total_stats', {}),
            'courses': dashboard_data.get('courses', {}),
            'students': dashboard_data.get('students', {})
        }
        
        return render(request, 'dashboard/dashboard.html', context)

