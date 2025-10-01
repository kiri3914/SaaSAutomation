from rest_framework import serializers

from .models import Mentor, Course
from ..students.serializers import GroupStudentSerializer


class MentorSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    direction_name = serializers.CharField(source='direction.title', read_only=True)
    class Meta:
        model = Mentor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'telegram',
                  'direction', 
                  'full_name', 
                  'branch', 
                  'branch_name',
                  'direction_name',
                  ]

        extra_kwargs = {
            'id': {'read_only': True},
            'full_name': {'read_only': True},
            'branch': {'read_only': True},
        }


class AdminMentorSerializer(MentorSerializer):
    class Meta:
        model = Mentor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'telegram',
                  'direction', 'full_name', 'branch']
        extra_kwargs = {
            'id': {'read_only': True},
            'full_name': {'read_only': True},
        }


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'direction',
                  'mentor', 'date_start', 'time_start', 'currency',
                  'time_end', 'telegram_group_link', 'branch',
                  'course_duration', 'price', 'description', 'is_active',
                  'count_students', 'current_month', 'next_month', 'finish_date', 'description']
        extra_kwargs = {
            'id': {'read_only': True},
            'count_students': {'read_only': True},
            'current_month': {'read_only': True},
            'next_month': {'read_only': True},
            'finish_date': {'read_only': True},
            'branch': {'read_only': True}
        }


class AdminCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'direction',
                  'mentor', 'date_start', 'time_start', 'currency',
                  'time_end', 'telegram_group_link', 'branch',
                  'course_duration', 'price', 'description', 'is_active',
                  'count_students', 'current_month', 'next_month', 'finish_date', 'description']
        extra_kwargs = {
            'id': {'read_only': True},
            'count_students': {'read_only': True},
            'current_month': {'read_only': True},
            'next_month': {'read_only': True},
            'finish_date': {'read_only': True},
        }


class GetCourseSerializer(serializers.ModelSerializer):
    student_course = GroupStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'direction', 'mentor', 'date_start', 'currency',
                  'time_start', 'time_end', 'telegram_group_link', 'branch',
                  'course_duration', 'price', 'description', 'is_active',
                  'count_students', 'current_month', 'next_month', 'finish_date', 'student_course']
