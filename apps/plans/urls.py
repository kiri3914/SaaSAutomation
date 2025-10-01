from django.urls import path
from .views import PlanningView, toggle_course_visibility, update_courses_order, export_planning

urlpatterns = [
    path('', PlanningView.as_view(), name='planning'),
    path('toggle/', toggle_course_visibility, name='toggle_course_visibility'),
    path('reorder/', update_courses_order, name='update_courses_order'),
    path('export/', export_planning, name='export_planning'),
] 