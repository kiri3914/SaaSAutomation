from django.utils.datetime_safe import datetime

from dateutil.relativedelta import relativedelta


class CourseDate:
    def __init__(self, date_start, course_duration):
        self.date_start = date_start
        self.course_duration = course_duration
        self.today = datetime.now().date()

    def current_month_course(self) -> int:
        """Возвращает количество прошедших месяцев с начала курса"""
        delta = relativedelta(self.today, self.date_start)
        return delta.years * 12 + delta.months + 1  # +1 так как отсчет начинается с нуля

    def finish_date(self) -> datetime:
        """Возвращает дату окончания курса"""
        return self.date_start + relativedelta(months=self.course_duration)

    def next_month(self) -> str:
        """Возвращает Дату начало следующего месяца или сообщение о завершении курса"""
        current = self.current_month_course()
        if current == self.course_duration:
            return 'Это последний месяц'
        elif self.today > self.finish_date():
            return 'Курс уже завершился'
        elif self.today < self.date_start:
            return self.date_start
        else:
            return self.date_start + relativedelta(months=current)

    def current_month(self) -> str:
        """Возвращает Текущий месяц"""
        current = self.current_month_course()
        if self.today > self.finish_date():
            return 'Курс уже завершился'
        elif self.today < self.date_start:
            return 'Курс ещё не начался'
        else:
            return f"{current}-месяц"
