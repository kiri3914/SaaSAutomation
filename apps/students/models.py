from django.db import models
from django.db.models import Sum
from django.forms import ValidationError

from apps.mainapp.models import Course
from apps.users.models import CustomUser
from . import utils

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    start_mount = models.IntegerField(default=1, validators=[utils.validate_positive], help_text='по умолчанию 1')
    email = models.EmailField(unique=True, help_text='Обязательное поле')
    discount = models.FloatField(default=0, blank=True, null=True, verbose_name="Скидка в Процентрах", help_text='по умолчанию 0')
    discount_of_cash = models.FloatField(default=0,  blank=True, null=True, verbose_name="сумма скидки", help_text='по умолчанию 0')
    phone = models.CharField(max_length=255, blank=True, null=True,
                             help_text='не обязательно, при записи введите номер в международном формате')
    whatsapp = models.CharField(max_length=255, blank=True, null=True,
                                help_text='не обязательно, при записи введите номер в международном формате')
    telegram = models.CharField(max_length=255, blank=True, null=True, help_text='не обязательно',
                                verbose_name='Телеграм')
    course: Course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='student_course')
    studies = models.BooleanField(default=True, verbose_name='Учится в настоящее время')
    comment = models.TextField(blank=True, null=True, help_text='не обязательно')
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recruited_students')
    create_at = models.DateTimeField(auto_now_add=True)
    contract = models.BooleanField(default=False, verbose_name='Договор')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['-studies', '-create_at']

    def clean(self):
        if self.discount and self.discount_of_cash:
            raise ValidationError('Вы можете выбрать только один вид скидки ПРОЦЕНТ или CУММУ!!!')

    @property
    def full_discount(self):
        """Возвращает полную скидку если в процентах то процент иначе сумму"""
        return f'{self.discount}%' if self.discount else f"{self.discount_of_cash} {self.currency}"

    @property
    def remainder_for_current_mount(self):
        """Сколько нужно оплатить за текущий месяц, если студент не учится то подсчет останавливается"""
        if not self.studies:
            return 0
        return utils.payment_for_current_mount(self)

    @property
    def payment(self):
        """Оплата высчитывается суммой всех платежей совершенных студентом"""
        payments = self.student_payment.aggregate(Sum('sum'))['sum__sum']
        if payments:
            return payments
        return 0

    @property
    def full_payment(self):
        """Общая сумма за весь курс, если студент не учится то подсчет останавливается"""
        if self.discount:
            full_price = self._count_mount(self) * self.course.price
            return float(full_price) - (float(full_price) * (self.discount / 100))
        elif self.discount_of_cash:
            full_price = self._count_mount(self) * self.course.price
            return float(full_price) - float(self.discount_of_cash)
        else:
            full_price = self._count_mount(self) * self.course.price
            return float(full_price)

    @property
    def remainder(self):
        """Общий остаток за весь курс, если студент не учится то подсчет останавливается"""
        if not self.studies:
            return 0
        return self.full_payment - self.payment

    @property
    def currency(self):
        """Возвращает валюту студента"""
        return self.course.branch.currency

    @property
    def branch_id(self):
        return self.course.branch.id if self.course else None

    @property
    def course_id(self):
        return self.course.id if self.course else None

    @staticmethod
    def _count_mount(self) -> int:
        """При вычислении отнимается 1 так как курс будет стартовать с нулевого месяца"""
        return self.course.course_duration - (self.start_mount - 1)

    def __str__(self):
        return f'Студент: {self.full_name} курс: {self.course.title}'


class PaymentStudent(models.Model):
    student: Student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_payment')
    sum = models.IntegerField()
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recruiter_payment')
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True, help_text='не обязательно')
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-date']

    @property
    def currency(self):
        return self.student.currency

    @property
    def branch(self):
        return self.student.course.branch

    def __str__(self):
        return f"{self.student.full_name} {self.sum}"
