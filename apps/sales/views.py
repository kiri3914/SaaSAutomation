from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import Client, ClientStatus, TrailLesson
from .serializers import ClientSerializer, ClientStatusSerializer, TrailLessonSerializer
from ..utils.base_views import BaseQuerysetView


class ClientModelViewSet(BaseQuerysetView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    related_name_filter = 'recruiter__branch'


class TrailLessonModelViewSet(BaseQuerysetView):
    queryset = TrailLesson.objects.all()
    serializer_class = TrailLessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch_id']


class ClientStatusModelViewSet(ModelViewSet):
    queryset = ClientStatus.objects.all()
    serializer_class = ClientStatusSerializer
