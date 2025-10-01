from django.contrib import admin
from .models import Student, PaymentStudent
from ..mainapp.models import Course
from import_export.admin import ImportExportModelAdmin


class PaymentInline(admin.TabularInline):
    fk_name = 'student'
    model = PaymentStudent
    extra = 1


class ActiveCourseListFilter(admin.SimpleListFilter):
    title = "Активные курсы"
    parameter_name = "active_courses"

    def lookups(self, request, model_admin):
        courses = Course.objects.filter(is_active=True)
        return [(course.id, f'{course.title} - {course.branch.city}') for course in courses]

    def queryset(self, request, queryset):
        selected_course_id = self.value()
        if selected_course_id and selected_course_id != 'active':
            return queryset.filter(course__id=selected_course_id)
        elif self.value() == "active":
            return queryset.filter(is_active=True)
        return queryset


class StudentAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'payment', 'discount', 'recruiter', 'contract', 'course')
    search_fields = ('full_name', 'comment', 'phone', 'telegram')
    list_editable = ('contract',)
    list_filter = (ActiveCourseListFilter, 'create_at', 'course__branch', 'studies')
    icon_name = 'people'


admin.site.register(Student, StudentAdmin)


@admin.register(PaymentStudent)
class PaymentStudentAdmin(ImportExportModelAdmin):
    list_display = ('student', 'branch', 'sum', 'currency', 'date', 'recruiter', 'comment')
    icon_name = 'attach_money'
