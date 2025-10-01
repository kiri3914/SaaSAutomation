from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Sum
from .servaice import CourseManager
from .utils import CourseDate
from ..branches.models import Branch, Direction
from ..students.utils import valid_phone, valid_telegram

class Mentor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, help_text='Обязательное поле')
    phone = models.CharField(max_length=255, null=True, blank=True, validators=[valid_phone])
    telegram = models.CharField(max_length=255, null=True, blank=True, validators=[valid_telegram])
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL,
                                  related_name='mentor_dir', null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name
    @property
    def branch_id(self):
        return self.branch.id if self.branch else None

    def __str__(self):
        return self.full_name


class Course(models.Model):
    title = models.CharField(max_length=100)
    direction = models.ForeignKey(
        Direction, on_delete=models.CASCADE, related_name='course_dir', verbose_name='Направление')
    mentor = models.ForeignKey(
        Mentor, on_delete=models.SET_NULL, related_name='course_mentor', null=True, blank=True)
    date_start = models.DateField(verbose_name='Старт группы')
    time_start = models.TimeField(verbose_name="Начало занятий")
    time_end = models.TimeField(verbose_name="Конец занятий")
    telegram_group_link = models.URLField(verbose_name='Ссылка на группу телеграм', null=True, blank=True)
    course_duration = models.PositiveIntegerField(verbose_name='Длительность курса в месяцах')
    price = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена за месяц')
    description = models.TextField(null=True, blank=True)
    branch: Branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False, auto_created=True)

    _date_object = None
    objects = CourseManager()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-date_start']

    @property
    def date_object(self):
        if self._date_object is None:
            self._date_object = CourseDate(date_start=self.date_start, course_duration=self.course_duration)
        return self._date_object

    @property 
    def count_students(self):
        return self.student_course.count()
    
    @property
    def count_active_students(self):
        return self.student_course.filter(studies=True).count()

    @property
    def current_month(self):
        return self.date_object.current_month()

    @property
    def current_month_course(self):
        return self.date_object.current_month_course()

    @property
    def next_month(self):
        """
        response type: date or str

        Возвращает Дату начало следующего месяца 
        или сообщение о завершении курса
        """
        return self.date_object.next_month()

    @property
    def finish_date(self):
        return self.date_object.finish_date()

    @property
    def currency(self):
        return self.branch.currency
    
    @property
    def fill_rate(self):
        """
        Возвращает процент заполненности группы
        """
        max_size = settings.MAX_GROUP_SIZE
        current_students = self.student_course.filter(studies=True).count()
        if max_size > 0:
            return int((current_students * 100) / max_size)
        return 0

    @property
    def sum_for_next_month(self):
        """
        Возвращает сумму задолженности за следующий месяц
        """
        debtors = self.student_course.filter(studies=True)
        return sum([s.remainder_for_current_mount for s in debtors if s.remainder_for_current_mount > 0])

    @property
    def get_recruitment_history(self):
        from datetime import datetime, timedelta
        students = self.student_course.filter(studies=True).order_by('create_at')
        if not students:
            return []
        
        result = []
        count = 0
        
        # Получаем первую и последнюю даты
        start_date = students.first().create_at.date()
        end_date = datetime.now().date()
        
        current_date = start_date
        while current_date <= end_date:
            # Считаем студентов на эту дату
            day_students = students.filter(create_at__date__lte=current_date).count()
            if day_students > 0:  # Добавляем только дни, когда были студенты
                result.append({
                    'date': current_date,
                    'count': day_students
                })
            current_date += timedelta(days=1)
        
        # Если нет данных за сегодня, добавляем текущее количество
        if not result or result[-1]['date'] < end_date:
            result.append({
                'date': end_date,
                'count': students.count()
            })
        
        return result
    
    def __str__(self):
        return f"курс по {self.title} c {self.date_start}"
    
    def clean(self) -> None:
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return super().clean()
