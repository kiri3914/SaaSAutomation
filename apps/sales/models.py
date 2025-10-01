from django.db import models

from apps.branches.models import Branch
from apps.mainapp.models import Mentor, Direction
from apps.students.utils import valid_phone
from apps.users.models import CustomUser


class TrailLesson(models.Model):
    title = models.CharField(max_length=100)
    directions = models.ManyToManyField(Direction, related_name='trail_lesson_dirs', verbose_name='Направление')
    mentors = models.ManyToManyField(Mentor, related_name='trail_lesson_mentors')
    recruiter = models.ManyToManyField(CustomUser, related_name='trail_lesson_recruiter')
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='trail_lesson_branch')

    class Meta:
        verbose_name = 'Пробный урок'
        verbose_name_plural = 'Пробные уроки'

    @property
    def count_clients(self):
        return Client.objects.filter(trail_lesson_id=self.pk).count()

    def __str__(self):
        return f'{self.title} - {self.date.date().strftime("%B %d")}'


class ClientStatus(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Статус клиента'
        verbose_name_plural = 'Статусы клиентов'

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True, validators=[valid_phone])
    whatsapp = models.CharField(max_length=255, blank=True, null=True, validators=[valid_phone],
                                verbose_name='whatsapp')
    trail_lesson = models.ForeignKey(TrailLesson, on_delete=models.SET_NULL,
                                     related_name='client_trail_lesson', null=True, blank=True)
    status = models.ForeignKey(ClientStatus, on_delete=models.SET_NULL, null=True,
                               related_name='client_status')
    comment = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='client_recruiter')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f"{self.name} {self.status} {self.create_at}"
