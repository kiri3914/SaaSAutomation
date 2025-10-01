from django import forms
from .models import Course
from datetime import datetime
from django.contrib.auth.models import User

# Определяем общие классы для форм
form_input_class = 'mt-1 block w-full px-4 py-3 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white text-base'
form_select_class = 'mt-1 block w-full px-4 py-3 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white text-base'
form_checkbox_class = 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'

class CourseForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если пользователь не суперпользователь, скрываем поле филиала
        if user and not user.is_superuser:
            self.fields['branch'].initial = user.branch
            self.fields['branch'].widget.attrs['readonly'] = True
            self.fields['branch'].widget.attrs['disabled'] = True
            self.fields['branch'].required = False
            # Фильтруем менторов по филиалу пользователя
            self.fields['mentor'].queryset = self.fields['mentor'].queryset.filter(branch=user.branch)

        # Преобразуем дату в формат HTML5 date input
        if self.instance.date_start:
            self.initial['date_start'] = self.instance.date_start.strftime('%Y-%m-%d')

    def clean_course_duration(self):
        course_duration = self.cleaned_data.get('course_duration')
        if course_duration < 1:
            raise forms.ValidationError("Длительность курса не может быть меньше 1 месяца")
        return course_duration
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price
    
    
    def clean_time_end(self):
        time_end = self.cleaned_data.get('time_end')
        time_start = self.cleaned_data.get('time_start')
        if time_end < time_start:
            raise forms.ValidationError("Время окончания не может быть раньше времени начала")
        return time_end
    
    
    class Meta:
        model = Course
        fields = ['title', 'direction', 'mentor', 'branch', 'description', 'price', 
                 'date_start', 'time_start', 'time_end', 'course_duration']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': form_input_class,
                'placeholder': 'Введите название курса'
            }),
            'direction': forms.Select(attrs={
                'class': form_select_class
            }),
            'mentor': forms.Select(attrs={
                'class': form_select_class
            }),
            'branch': forms.Select(attrs={
                'class': form_select_class
            }),
            'description': forms.Textarea(attrs={
                'class': form_input_class,
                'rows': 4,
                'placeholder': 'Описание курса'
            }),
            'price': forms.NumberInput(attrs={
                'class': form_input_class,
                'placeholder': '140000.00'
            }),
            'date_start': forms.DateInput(attrs={
                'class': form_input_class,
                'type': 'date'
            }),
            'time_start': forms.TimeInput(attrs={
                'class': form_input_class,
                'type': 'time'
            }),
            'time_end': forms.TimeInput(attrs={
                'class': form_input_class,
                'type': 'time'
            }),
            'course_duration': forms.NumberInput(attrs={
                'class': form_input_class,
                'min': 1
            }),
        }
        labels = {
            'title': 'Название курса',
            'direction': 'Направление',
            'mentor': 'Ментор',
            'branch': 'Филиал',
            'description': 'Описание',
            'price': 'Стоимость',
            'date_start': 'Дата начала',
            'time_start': 'Время начала',
            'time_end': 'Время окончания', 
            'course_duration': 'Длительность (месяцев)'
        }