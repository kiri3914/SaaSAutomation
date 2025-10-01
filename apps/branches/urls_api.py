from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, BranchViewSet, DirectionViewSet

router = DefaultRouter()
router.register('direction', DirectionViewSet, basename='Direction')
router.register('countries', CountryViewSet)
router.register('branches', BranchViewSet)

urlpatterns = router.urls
