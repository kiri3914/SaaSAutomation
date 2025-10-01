from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('payment_students', views.PaymentStudentViewSet)

urlpatterns = router.urls