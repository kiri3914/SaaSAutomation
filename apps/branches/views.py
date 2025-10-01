from rest_framework.viewsets import ModelViewSet

from .serializer import CountrySerializer, BranchSerializer, DirectionSerializer
from .models import Country, Branch, Direction
from .permissions import CountyPermission, BranchPermission, DirectionPermission
from ..utils.base_views import BaseQuerysetView


class DirectionViewSet(BaseQuerysetView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [DirectionPermission]

    related_name_filter = 'directions_branch'


class CountryViewSet(BaseQuerysetView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CountyPermission]

    related_name_filter = 'branch_country'


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [BranchPermission]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super().get_queryset()
            if not self.request.user.branch:
                return self.queryset.model.objects.none()
            return self.queryset.model.objects.filter(id=self.request.user.branch.id)
        return self.queryset.model.objects.none()
