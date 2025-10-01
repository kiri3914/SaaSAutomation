from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sales'
    verbose_name = 'Продажи'
    icon_name = 'attach_money'

    def ready(self):
        # импортировать файл signals.py
        from apps.sales import signals
