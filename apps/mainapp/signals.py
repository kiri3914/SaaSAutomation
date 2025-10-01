from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course

# from ..utils.push_notification import send_message_telebot


@receiver(post_save, sender=Course)
def push_handler(sender, instance, created, **kwargs):
    if not instance.is_active and not instance.notified:
        text = f'Группа  {instance.title} успешно выпущен!'
        chat_id = instance.branch.chat_id
        # send_message_telebot(text=text, chat_id=chat_id)
        student_course = instance.student_course.all()
        for student in student_course:
            if student.studies:
                student.studies = False
                if not student.comment:
                    student.comment = 'Успешно выпустился(ась)'
                else:
                    student.comment += '\nУспешно выпустился(ась)'
                student.save()
        instance.notified = True
        instance.save()
