from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mainapp'
    verbose_name = 'Главная'
    icon_name = 'apps'

    def ready(self):
        from . import signals
