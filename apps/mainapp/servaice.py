from datetime import timedelta, date as dt

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from apps.utils.push_notification import send_message_telebot


class CourseManager(models.Manager):
    def notify_upcoming_courses(self):
        """Уведомляет о предстоящих курсах"""

        upcoming_courses = self.get_upcoming_courses()
        for course in upcoming_courses:
            days_left = (course.next_month - now().date()).days
            if days_left == 1:
                text_days_left = "завтра."
            else:
                text_days_left = f"через {days_left} дня."

            subject = "Уведомление о предстоящих курсах!"
            message = f'Хотели бы напомнить вам о том, что {course.current_month_course+1}-месяц обучения курса \
            \n"{course.title}" начинается {text_days_left} ({course.next_month})\
            \n\n🚨 Срочно соберите оплату !!! .\
            \n\nС уважением,\nКоманда {settings.PROJECT_NAME}'
            chat_id = course.branch.chat_id
            text = subject + '\n\n' + message
            send_message_telebot(text=text, chat_id=chat_id)

    def get_upcoming_courses(self) -> list:
        today = now().date()
        courses = self.filter(is_active=True)
        upcoming_courses = []
        for course in courses:
            if isinstance(course.next_month, dt):
                if course.next_month == today + timedelta(days=1) \
                        or course.next_month == today + timedelta(days=3):
                    upcoming_courses.append(course)
        return upcoming_courses
