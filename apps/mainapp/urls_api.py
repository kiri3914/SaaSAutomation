from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('mentor', views.MentorViewSet, basename='Mentor')
router.register('course', views.CourseViewSet, basename='Course')

urlpatterns = router.urls