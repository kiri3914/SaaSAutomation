from django.core.management.base import BaseCommand
from apps.mainapp.models import Course


class Command(BaseCommand):
    help = 'Уведомление о предстоящих курсах'

    def handle(self, *args, **options):
        Course.objects.notify_upcoming_courses()
        self.stdout.write(self.style.SUCCESS('Уведомления успешно отправлены!'))
