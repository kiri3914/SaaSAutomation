from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Mentor,
    Course,
)


@register(Mentor)
class MentorAdmin(ImportExportModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'telegram',
        'direction',
        'branch')
    icon_name = 'assignment_ind'


@register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = (
        'title',
        'direction',
        'mentor',
        'date_start',
        'time_start',
        'time_end',
        'telegram_group_link',
        'course_duration',
        'price',
        'branch',
        'is_active',
    )
    icon_name = 'laptop_mac'
