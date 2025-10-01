from django.urls import path
from .views import CoursesBasePageView, StudentsBasePageView, DashboardView

urlpatterns = [
    path('courses', CoursesBasePageView.as_view()),
    path('students', StudentsBasePageView.as_view()),
    path('', DashboardView.as_view(), name='dashboard'),
]

