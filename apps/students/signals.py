from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student, PaymentStudent

# from ..utils.push_notification import send_message_telebot


@receiver(post_save, sender=Student)
def create_student(sender, instance, created, **kwargs):
    if created:
        # отправить уведомление только при создании объекта Student
        text = f"Добавлен новый студент!" \
               f"\nИмя:    {instance.full_name}" \
               f"\nГруппа: {instance.course.title}" \
               f"\nРекрут: {instance.recruiter.username}" \
               f"\nКомментарий: {instance.comment}" \
               f"\n\nС уважением, \nКоманда Itc service."
        chat_id = instance.course.branch.chat_id
        # send_message_telebot(text=text, chat_id=chat_id)


@receiver(post_save, sender=PaymentStudent)
def create_payment(sender, instance, created, **kwargs):
    if created:
        # отправить уведомление только при создании объекта PaymentStudent
        text = f"Принята оплата!" \
               f"\nСтудент: {instance.student.full_name}" \
               f"\nГруппа: {instance.student.course}" \
               f"\nСумма:   {instance.sum} {instance.student.currency}" \
               f"\nРекрут:  {instance.recruiter.username}" \
               f"\nКомментарий: {instance.comment}" \
               f"\n\nС уважением, \nКоманда Itc service."
        chat_id = instance.student.course.branch.chat_id
        # send_message_telebot(text=text, chat_id=chat_id)


@receiver(post_delete, sender=Student)
def delete_student(sender, instance, **kwargs):
    # выполнить дополнительные действия после удаления экземпляра модели MyModel
    text = f"Студент(ка) {instance.full_name} был(а) удален(а) из группы {instance.course.title}" \
           f"\nКомментарий: {instance.comment}" \
           f"\n\nС уважением, \nКоманда Itc service."
    chat_id = instance.course.branch.chat_id
    # send_message_telebot(text=text, chat_id=chat_id)


@receiver(post_save, sender=Student)
def off_student(sender, instance, created, **kwargs):
    if not instance.studies:
        # отправить уведомление при отключении студента
        text = f"Студент(ка) {instance.full_name} больше не состоит в группе {instance.course.title}" \
               f"\nКомментарий: {instance.comment}" \
               f"\n\nС уважением, \nКоманда Itc service."
        chat_id = instance.course.branch.chat_id
        # send_message_telebot(text=text, chat_id=chat_id)
