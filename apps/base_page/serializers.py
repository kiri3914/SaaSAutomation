from django.conf import settings

from rest_framework import serializers

from apps.mainapp.models import Course
from apps.students.models import Student


class GetCourseBasePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'date_start',
            'count_students'
        ]

class ActiveGroupsFillRateSerializer(serializers.ModelSerializer):
    fill_rate = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'date_start', 'count_students', 'fill_rate']

    def get_fill_rate(self, obj):
        if obj.count_students > 0:
            return round((obj.count_students / settings.MAX_GROUPS_SIZE) * 100, 2)
        return 0  


class GetGroupsStartingNextMonthWithinWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'date_start', 'count_students', 'next_month']

class GetStudentsBasePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'course', 'remainder_for_current_mount']


class GetDebtorStudentsBasePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'course', 'remainder_for_current_mount']

