from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.contrib import messages
from rest_framework.response import Response
from .permissions import CourseAndMentorPermission
from .models import Mentor, Course
from ..students.models import Student

from .serializers import MentorSerializer, CourseSerializer, GetCourseSerializer, AdminCourseSerializer, \
    AdminMentorSerializer

from ..students.serializers import StudentSerializer

from ..utils.base_views import BaseQuerysetView
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import CourseForm


@login_required
def course_edit(request, pk):
    course = Course.objects.get(id=pk)
    if not request.user.is_superuser and course.branch != request.user.branch:
        raise PermissionDenied
    if request.method == 'POST':
        print("POST data:", request.POST)  # Отладочная информация
        form = CourseForm(user=request.user, data=request.POST, instance=course)
        if form.is_valid():
            print("Form is valid")  # Отладочная информация
            print("Cleaned data:", form.cleaned_data)  # Отладочная информация
            course = form.save(commit=False)
            if not request.user.is_superuser:
                course.branch = request.user.branch
            course.save()
            messages.success(request, 'Курс успешно обновлен')
            return redirect('course_detail', pk=course.id)
        else:
            print("Form errors:", form.errors)  # Отладочная информация
    else:
        form = CourseForm(user=request.user, instance=course)
        if not request.user.is_superuser:
            form.initial['branch'] = request.user.branch
    return render(request, 'mainapp/course_form.html', {'form': form, 'course': course})
@login_required
def course_delete(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect('dashboard')
@login_required
def finish_course(request, pk):
    course = Course.objects.get(id=pk)
    course.is_active = False
    course.save()
    messages.success(request, f'Курс {course.title} успешно завершен')
    return redirect('course_detail', pk=course.id)

@login_required
def course_create(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = CourseForm(user=request.user, data=request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            if not request.user.is_superuser:
                course.branch = request.user.branch
            course.save()
            messages.success(request, 'Курс успешно создан')
            return redirect('course_detail', pk=course.id)
    else:
        form = CourseForm(user=request.user)
        if not request.user.is_superuser:
            form.initial['branch'] = request.user.branch
    return render(request, 'mainapp/course_form.html', {'form': form})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, id=pk)
    active_students = Student.objects.filter(course=course, studies=True)
    archived_students = Student.objects.filter(course=course, studies=False)
    
    context = {
        'course': course,
        'active_students': active_students,
        'archived_students': archived_students,
        'total_students': active_students.count() + archived_students.count(),
        'active_students_count': active_students.count(),
        'archived_students_count': archived_students.count(),
        'debtors': [s for s in active_students if s.remainder_for_current_mount > 0],
        'no_contract': active_students.filter(contract=False),
    }
    
    return render(request, 'mainapp/course_detail.html', context)


class MentorViewSet(BaseQuerysetView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [CourseAndMentorPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch_id', 'id', 'direction_id', 'email', 'phone', 'telegram']

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:

            serializer = AdminMentorSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_staff and request.user.branch is not None:
            serializer = MentorSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(branch=self.request.user.branch)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'У вас не достаточно прав для создания'}, status=403)


class CourseViewSet(BaseQuerysetView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'direction_id', 'is_active', 'branch_id']
    permission_classes = [CourseAndMentorPermission]
    related_name_filter = 'branch'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = AdminCourseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_staff and request.user.branch is not None:
            serializer = CourseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(branch=self.request.user.branch)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'У вас не достаточно прав для создания'}, status=403)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetCourseSerializer(instance)
        return Response(serializer.data)


class CourseAdminViewSet(BaseQuerysetView):
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [CourseAndMentorPermission]
    
    def get_course_detail(self, course_id):
        """Get detailed course information"""
        course = self.get_object()
        students = Student.objects.filter(course=course)
        return {
            'course': self.get_serializer(course).data,
            'students': StudentSerializer(students, many=True).data
        }

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        return Response(self.get_course_detail(pk))

    @action(detail=True, methods=['post']) 
    def delete_course(self, request, pk=None):
        course = self.get_object()
        course.delete()
        return Response(status=204)
