from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RecruiterDetailView
from django.contrib.auth.decorators import user_passes_test

def is_admin_or_branch_admin(user):
    return user.is_superuser or user.is_branch_admin

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
      # Сброс пароля
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('recruiter/<int:pk>/', 
         user_passes_test(is_admin_or_branch_admin)(RecruiterDetailView.as_view()), 
         name='recruiter_detail'),
]


