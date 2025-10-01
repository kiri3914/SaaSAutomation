from rest_framework import serializers
from .models import Country, Branch, Direction


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'title', 'description']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class BranchSerializer(serializers.ModelSerializer):
    list_direction = DirectionSerializer(many=True)

    class Meta:
        model = Branch
        fields = ('id', 'country', 'city', 'address', 'opening_date', 'instagram', 'whatsapp', 'list_direction')
