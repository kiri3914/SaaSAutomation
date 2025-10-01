from django.urls import path
from . import views


urlpatterns = [
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('create_contract/<int:pk>/', views.create_contract, name='create_contract'),
    path('student/create/<int:course_id>/', views.student_create, name='student_create'),
    path('student_edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('student_delete/<int:pk>/', views.student_delete, name='student_delete'),
    
    path('payment_create/<int:pk>/', views.payment_create, name='payment_create'),
    path('payment_edit/<int:pk>/', views.payment_edit, name='payment_edit'),
    path('payment_delete/<int:pk>/', views.payment_delete, name='payment_delete'),
    path('archive_student/<int:pk>/', views.archive_student, name='archive_student'),
    path('create_receipt/<int:pk>/', views.create_receipt, name='create_receipt'),
]

