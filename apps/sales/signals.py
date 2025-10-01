from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client

from ..utils.push_notification import send_message_telebot


@receiver(post_save, sender=Client)
def create_student(sender, instance, created, **kwargs):
    if created:
        # отправить уведомление только при создании объекта Student
        text = f"Добавлен новый Клиент на Пробный урок!" \
               f"\nИмя:    {instance.name}" \
               f"\nПробный урок: {instance.trail_lesson}" \
               f"\nРекрут: {instance.recruiter.username}" \
               f"\nКомментарий: {instance.comment}"\
               f"\n\nС уважением, \nКоманда Itc service."
        chat_id = instance.trail_lesson.branch.chat_id
        send_message_telebot(text=text, chat_id=chat_id)
