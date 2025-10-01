from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.course_create, name='course_create'),
    path('course_detail/<int:pk>/', views.course_detail, name='course_detail'),
    path('course_edit/<int:pk>/', views.course_edit, name='course_edit'),
    path('delete_course/<int:pk>/', views.course_delete, name='course_delete'),
    path('finish_course/<int:pk>/', views.finish_course, name='finish_course')
]

