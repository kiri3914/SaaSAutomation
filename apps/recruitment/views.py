from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from datetime import datetime, timedelta
from apps.mainapp.models import Course, Branch, Direction
from django.db.models import Count, Q
import math

class RecruitmentView(LoginRequiredMixin, TemplateView):
    template_name = 'recruitment/recruitment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MAX_GROUP_SIZE'] = settings.MAX_GROUP_SIZE
        branch_id = self.request.GET.get('branch_id')
        
        if not branch_id:
            branch_id = self.request.user.branch_id if self.request.user.branch_id else Branch.objects.first().id
        else:
            branch_id = int(branch_id)
            
        active_recruitments = Course.objects.filter(
            branch_id=branch_id,
            is_active=True,
            date_start__gt=datetime.now().date()
        ).annotate(
            student_count=Count('student_course', filter=Q(student_course__studies=True))
        ).order_by('date_start')

        recruitment_plans = []
        today = datetime.now().date()
        total_current_students = 0
        total_students_needed = 0
        total_weekly_goal = 0
        
        for course in active_recruitments:
            days_until_start = (course.date_start - today).days
            weeks_until_start = math.ceil(days_until_start / 7)
            
            if weeks_until_start <= settings.WEEKS_BEFORE_START:
                students_needed = settings.MAX_GROUP_SIZE - course.student_count
                if students_needed > 0:
                    weekly_goal = max(1, students_needed // weeks_until_start)
                    
                    history = course.get_recruitment_history
                    weeks_breakdown = []
                    current_week_start = today - timedelta(days=today.weekday())
                    for i in range(weeks_until_start):
                        week_start = current_week_start + timedelta(days=i * 7)
                        week_end = min(week_start + timedelta(days=6), course.date_start - timedelta(days=1))
                        
                        actual = course.student_count
                        if history:
                            actual = max([h['count'] for h in history if h['date'] <= week_end] or [course.student_count])
                        if week_end > today:
                            actual = course.student_count
                        
                        target = min(settings.MAX_GROUP_SIZE, course.student_count + (weekly_goal * (i + 1)))
                        
                        weeks_breakdown.append({
                            'week': i + 1,
                            'target': target,
                            'actual': actual,
                            'start_date': week_start,
                            'end_date': week_end,
                        })
                    
                    recruitment_plans.append({
                        'course': course,
                        'weeks_left': weeks_until_start,
                        'current_students': course.student_count,
                        'students_needed': students_needed,
                        'weekly_goal': weekly_goal,
                        'progress_percentage': int((course.student_count * 100) / settings.MAX_GROUP_SIZE),
                        'weeks_breakdown': weeks_breakdown,
                        'recent_students': course.student_course.filter(studies=True).order_by('-create_at')[:5],
                        'recruitment_history': [{'date': h['date'].strftime('%d.%m'), 'count': h['count']} for h in history],
                    })
                    
                    # Агрегированные данные
                    total_current_students += course.student_count
                    total_students_needed += students_needed
                    total_weekly_goal += weekly_goal

        # Общая статистика
        total_courses = len(recruitment_plans)
        overall_progress = int((total_current_students * 100) / (total_courses * settings.MAX_GROUP_SIZE)) if total_courses > 0 else 0

        context.update({
            'recruitment_plans': recruitment_plans,
            'selected_branch_id': branch_id,
            'branches': Branch.objects.all(),
            'total_courses': total_courses,
            'total_current_students': total_current_students,
            'total_students_needed': total_students_needed,
            'total_weekly_goal': total_weekly_goal,
            'overall_progress': overall_progress,
        })
        return context