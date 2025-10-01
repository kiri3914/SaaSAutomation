from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncMonth
from datetime import datetime
from apps.mainapp.models import Course, Direction
from apps.branches.models import Branch
from apps.students.models import Student
from apps.users.models import CustomUser
from django.conf import settings
from django.utils import timezone

class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'statistics/statistics.html'
    
    def format_money(self, amount, branch):
        """Форматирует денежную сумму с учетом валюты филиала"""
        if amount is None:
            amount = 0
        formatted = f"{amount:,.0f}".replace(",", " ")
        return f"{formatted} {branch.currency}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch_id = self.request.GET.get('branch_id')
        
        if not branch_id:
            branch_id = self.request.user.branch_id if self.request.user.branch_id else Branch.objects.first().id
        else:
            branch_id = int(branch_id)
            
        branch = Branch.objects.get(id=branch_id)
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_date = timezone.now()
        
        # Статистика по студентам
        students = Student.objects.filter(course__branch_id=branch_id)
        active_students = students.filter(studies=True)
        
        student_stats = {
            'total_active': active_students.count(),
            'new_this_month': students.filter(
                create_at__month=current_month,
                create_at__year=current_year
            ).count(),
            'left_this_month': students.filter(
                studies=False,
                create_at__month=current_month,
                create_at__year=current_year
            ).count(),
            'by_course': active_students.values(
                'course__title'
            ).annotate(count=Count('id')).order_by('-count')
        }

        # Финансовая статистика
        month_payments = sum([
            payment.sum 
            for student in active_students
            for payment in student.student_payment.filter(
                date__month=current_month,
                date__year=current_year
            )
        ])
        
        current_debts = sum([
            student.remainder_for_current_mount 
            for student in active_students 
            if student.remainder_for_current_mount > 0
        ])
        
        avg_payment = month_payments / active_students.count() if active_students.count() > 0 else 0
        
        financial_stats = {
            'month_income': self.format_money(month_payments, branch),
            'current_debts': self.format_money(current_debts, branch),
            'avg_payment': self.format_money(avg_payment, branch)
        }

        # Статистика по курсам
        courses = Course.objects.filter(branch_id=branch_id)
        active_courses = courses.filter(is_active=True)
        
        course_stats = {
            'total_active': active_courses.count(),
            'by_direction': active_courses.values(
                'direction__title'
            ).annotate(
                count=Count('id')
            ).order_by('-count'),
            'fill_rate': [
                {
                    'title': course.title,
                    'rate': course.fill_rate,
                    'current': course.student_course.filter(studies=True).count(),
                    'max': settings.MAX_GROUP_SIZE
                }
                for course in active_courses
            ]
        }

        # Тренды по месяцам (12 месяцев для графика)
        monthly_trends = Student.objects.filter(
            course__branch_id=branch_id
        ).annotate(
            month=TruncMonth('create_at')
        ).values('month').annotate(
            new_students=Count('id', distinct=True),
            income=Sum('student_payment__sum')
        ).order_by('-month')[:13]

        months = [month['month'].strftime('%B') for month in monthly_trends][::-1]
        sales = [month['income'] if month['income'] is not None else 0 for month in monthly_trends][::-1]
        students_by_month = [month['new_students'] for month in monthly_trends][::-1]

        # Статистика по рекрутерам
        recruiters = CustomUser.objects.filter(
            branch_id=branch_id,
            is_active=True
        )
        
        recruiter_stats = []
        for recruiter in recruiters:
            recruiter_students = Student.objects.filter(recruiter=recruiter)
            month_students = recruiter_students.filter(
                create_at__month=current_month,
                create_at__year=current_year
            )
            month_active_students = month_students.filter(studies=True)  # Активные студенты за месяц
            month_revenue = sum([
                payment.sum 
                for student in month_students
                for payment in student.student_payment.filter(
                    date__month=current_month,
                    date__year=current_year
                )
            ])
            active_students = recruiter_students.filter(studies=True)
            
            recruiter_stats.append({
                'id': recruiter.id,
                'name': recruiter.username,
                'total_students': recruiter_students.count(),
                'active_students': active_students.count(),
                'month_students': month_students.count(),
                'month_active_students': month_active_students.count(),
                'month_revenue': self.format_money(month_revenue, branch),
                'conversion_rate': int((month_active_students.count() / month_students.count() * 100) if month_students.count() > 0 else 0),
            })
            print(f'{recruiter.username} {active_students.count()}, {recruiter_students.count()}, {month_students.count()}, {month_active_students.count()},Итоговый  {int((month_active_students.count() / month_students.count() * 100) if month_students.count() > 0 else 0)}')

        course_stats['by_recruiters'] = sorted(recruiter_stats, key=lambda x: x['month_students'], reverse=True)

        context.update({
            'current_date': current_date,
            'student_stats': student_stats,
            'financial_stats': financial_stats,
            'course_stats': course_stats,
            'monthly_trends': monthly_trends,
            'selected_branch_id': branch_id,
            'branches': Branch.objects.all(),
            'branch': branch,
            'months': months,
            'sales': sales,
            'students_by_month': students_by_month,
        })
        return context