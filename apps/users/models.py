from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

from apps.branches.models import Branch


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, help_text='Обязательное поле', verbose_name='Email')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Номер телефона')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,blank=True, null=True, related_name='user_branches')

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self) -> str:
        return str(self.username)

    def clean(self):
        if self.branch and self.is_superuser:
            raise ValidationError('Администратор не может быть администратором филиала. (Чтобы быть администратором филиала, уберите флаг статус суперпользователя)')
    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_branch_admin(self):
        return self.branch is not None and not self.is_superuser

    @property
    def branch_id(self):
        return self.branch.id if self.branch else None