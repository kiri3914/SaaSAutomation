from django.urls import path
from .views import RecruitmentView

urlpatterns = [
    path('', RecruitmentView.as_view(), name='recruitment'),
] 