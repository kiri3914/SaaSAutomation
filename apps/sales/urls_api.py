from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('trail_lessons', views.TrailLessonModelViewSet)
router.register('clients', views.ClientModelViewSet)
router.register('client_status', views.ClientStatusModelViewSet)

urlpatterns = router.urls
