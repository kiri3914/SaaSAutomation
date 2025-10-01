from rest_framework import serializers

from .models import Client, ClientStatus, TrailLesson


class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class TrailLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailLesson
        fields = '__all__'

