from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Student, PaymentStudent
from .permissions import StudentPermission, PaymentsPermission
from .serializers import StudentSerializer, PaymentStudentSerializer
from .forms import StudentForm, PaymentForm
from ..mainapp.models import Course
from .utils import generate_pdf

from ..utils.base_views import BaseQuerysetView

@login_required
def create_receipt(request, pk):
    payment = get_object_or_404(PaymentStudent, id=pk)
    if payment.receipt:
        return redirect(payment.receipt.url)
    try:
        generate_pdf(payment)
        messages.success(request, f'Квитанция успешно создана')
        return redirect(payment.receipt.url)
    except Exception as e:
        messages.error(request, f'Ошибка при создании квитанции: {e}')
    return redirect('student_detail', pk=payment.student.id)

@login_required
def archive_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    if student.studies:
        student.studies = False
        student.save()
        messages.success(request, f'Студент {student.full_name} успешно перемещен в архив')
    else:
        student.studies = True
        student.save()
        messages.success(request, f'Студент {student.full_name} успешно возвращен из архива')
    return redirect('student_detail', pk=student.id)

@login_required
def create_contract(request, pk):
    try:
        student = Student.objects.get(id=pk)
        student.contract = True
        student.save()
    except Student.DoesNotExist:
        messages.error(request, 'Студент не найден')
        return redirect('dashboard')
    messages.success(request, f'Вы подписали договор с {student.full_name}')
    return redirect('student_detail', pk=student.id)

@login_required
def student_create(request, course_id=None):
    course = get_object_or_404(Course, id=course_id) if course_id else None
    
    if request.method == 'POST':
        form = StudentForm(request.POST, course=course)
        if form.is_valid():
            student = form.save()
            payment = form.cleaned_data.get('payment')
            payment_comment = form.cleaned_data.get('payment_comment')
            
            if payment:
                PaymentStudent.objects.create(
                    student=student,
                    sum=payment,
                    comment=payment_comment,
                    recruiter=student.recruiter
                )
            messages.success(request, f'Студент {student.full_name} успешно создан')
            return redirect('student_detail', student.id)
        else:
            # Обработка ошибок формы
            for field, errors in form.errors.items():
                if field == '__all__':
                    for error in errors:
                        messages.error(request, f'Ошибка: {error}')
                else:
                    for error in errors:
                        messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = StudentForm(course=course)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Создание студента',
        'is_edit': False
    })

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, id=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student, course=student.course)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Студент {student.full_name} успешно обновлен')
            return redirect('student_detail', pk=student.id)
        else:
            # Обработка ошибок формы
            for field, errors in form.errors.items():
                if field == '__all__':
                    for error in errors:
                        messages.error(request, f'Ошибка: {error}')
                else:
                    for error in errors:
                        messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = StudentForm(instance=student, course=student.course)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Редактирование студента',
        'is_edit': True
    })

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    messages.success(request, f'Студент {student.full_name} успешно удален')
    return redirect('course_detail', student.course.id)

@login_required
def payment_create(request, pk):
    student = get_object_or_404(Student, id=pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.recruiter = request.user
            payment.save()
            
            messages.success(request, f'Оплата на сумму {payment.sum} {payment.currency} успешно добавлена')
            return redirect('student_detail', pk=student.id)
    else:
        form = PaymentForm()
    
    return render(request, 'students/payment_form.html', {
        'form': form,
        'student': student,
        'title': 'Добавление оплаты',
        'is_edit': False
    })

@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(PaymentStudent, id=pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Оплата успешно обновлена')
            return redirect('student_detail', pk=payment.student.id)
    else:
        form = PaymentForm(instance=payment)
    
    return render(request, 'students/payment_edit.html', {
        'form': form,
        'payment': payment,
        'is_edit': True
    })

@login_required 
def payment_delete(request, pk):
    payment = get_object_or_404(PaymentStudent, id=pk)
    payment.delete()
    messages.success(request, f'Оплата на сумму {payment.sum} {payment.currency} успешно удалена')
    return redirect('student_detail', pk=payment.student.id)

class StudentViewSet(BaseQuerysetView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [StudentPermission]
    filterset_fields = ['course', 'phone', 'email', 'whatsapp', 'full_name', 'telegram', 'studies', 'recruiter']

    related_name_filter = 'course__branch'


class PaymentStudentViewSet(BaseQuerysetView):
    queryset = PaymentStudent.objects.all()
    serializer_class = PaymentStudentSerializer
    permission_classes = [PaymentsPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student']

    related_name_filter = 'student__course__branch'


class StudentAdminViewSet(BaseQuerysetView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentPermission]

    def get_student_detail(self, student_id):
        """Get detailed student information"""
        student = self.get_object()
        payments = PaymentStudent.objects.filter(student=student)
        return {
            'student': self.get_serializer(student).data,
            'payments': PaymentStudentSerializer(payments, many=True).data
        }

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        return Response(self.get_student_detail(pk))


class PaymentAdminViewSet(BaseQuerysetView):
    queryset = PaymentStudent.objects.all()
    serializer_class = PaymentStudentSerializer
    permission_classes = [PaymentsPermission]

