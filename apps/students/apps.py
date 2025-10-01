from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.students'
    verbose_name = 'Студенты'
    icon_name = 'people'

    def ready(self):
        # импортировать файл signals.py
        from apps.students import signals
