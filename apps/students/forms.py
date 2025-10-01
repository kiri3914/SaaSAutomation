from django import forms
from .models import Student, PaymentStudent
from apps.mainapp.models import Course
from apps.users.models import CustomUser
from apps.utils.number_validation import extract_and_normalize_phone


form_input_class = 'mt-1 block w-full px-4 py-3 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white text-base'
form_select_class = 'mt-1 block w-full px-4 py-3 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white text-base'

class StudentForm(forms.ModelForm):
    start_mount = forms.IntegerField(
        label='Месяц начала',
        min_value=1,
        max_value=12,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': form_input_class,
            'placeholder': 'Введите номер месяца (1-12)'
        })
    )
    
    discount = forms.IntegerField(
        required=False,
        label='Скидка в процентах',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите процент скидки',
            'class': form_input_class
        })
    )
    
    discount_of_cash = forms.DecimalField(
        required=False,
        label='Скидка в сумме',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите сумму скидки',
            'class': form_input_class
        })
    )

    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Добавьте комментарий',
            'class': form_input_class
        })
    )
    payment = forms.IntegerField(
        required=False,
        label='Сумма оплаты',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите сумму оплаты',
            'class': form_input_class
        })
    )

    payment_comment = forms.CharField(
        required=False,
        label='Комментарий к оплате',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Добавьте комментарий к оплате',
            'class': form_input_class
        })
    )
    contract = forms.BooleanField(
        required=False,
        label='Договор подписан',
        widget=forms.CheckboxInput(attrs={
            'class': form_input_class
        })
    )

    class Meta:
        model = Student
        fields = ['full_name', 'phone', 'email', 'whatsapp', 'telegram',
                 'course', 'start_mount', 'contract', 'recruiter',
                 'discount', 'discount_of_cash', 'comment', 'payment', 'payment_comment']
        required_fields = ['full_name', 'email', 'course', 'recruiter']

    def __init__(self, *args, course=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_instance = course
        self.course_title = course.title
        
        # Применяем стили к полям
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = form_select_class
            elif not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = form_input_class

        # Настройка поля course
        if course and not self.instance.pk:  # Если это создание нового студента
            self.fields['course'].initial = course
            self.fields['course'].widget.attrs['readonly'] = True
            self.fields['course'].widget = forms.Select(
                attrs={'class': form_select_class + ' bg-gray-100'},
                choices=[(course.id, f"{course.title}")]
            )
        else:  # Если это редактирование
            self.fields['course'].widget = forms.Select(
                attrs={'class': form_select_class},
                choices=[(c.id, f"{c.title} - {c.branch}") 
                        for c in Course.objects.select_related('branch').all()]
            )

        # Кастомные лейблы и плейсхолдеры
        self.fields['full_name'].label = 'ФИО'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Введите ФИО'
        
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].widget.attrs['placeholder'] = '+7 (XXX) XXX-XX-XX'
        
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs['placeholder'] = 'example@email.com'
        
        self.fields['whatsapp'].label = 'WhatsApp'
        self.fields['whatsapp'].widget.attrs['placeholder'] = 'Введите номер WhatsApp'
        
        self.fields['telegram'].label = 'Telegram'
        self.fields['telegram'].widget.attrs['placeholder'] = '@username'
        
        self.fields['course'].label = 'Курс'
        self.fields['contract'].label = 'Договор подписан'
        self.fields['recruiter'].label = 'Рекрутер'
        
        # Настройка поля recruiter
        if course:  # Если курс передан
            self.fields['recruiter'].widget = forms.Select(
                attrs={'class': form_select_class},
                choices=[(user.id, user.username) 
                        for user in CustomUser.objects.filter(is_active=True, branch=course.branch)]
            )
        else:  # Если курс не передан (например, при редактировании)
            self.fields['recruiter'].widget = forms.Select(
                attrs={'class': form_select_class},
                choices=[(user.id, user.username) 
                        for user in CustomUser.objects.filter(is_active=True)]
            )

    def clean_payment(self):
        payment = self.cleaned_data.get('payment')
        if payment and payment < 0:
            raise forms.ValidationError('Сумма оплаты не может быть отрицательной')
        return payment
    
    def clean_start_mount(self):
        start_mount = self.cleaned_data.get('start_mount')
        if start_mount and start_mount > self.course_instance.course_duration:
            raise forms.ValidationError('Месяц начала не может быть больше количества месяцев в курсе')
        return start_mount
    
    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if whatsapp:
            whatsapp = extract_and_normalize_phone(whatsapp)
            if not whatsapp:
                raise forms.ValidationError('Некорректный номер WhatsApp')
        return whatsapp
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = extract_and_normalize_phone(phone)
            if not phone:
                raise forms.ValidationError('Некорректный номер телефона')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        discount = cleaned_data.get('discount')
        discount_of_cash = cleaned_data.get('discount_of_cash')

        if discount and discount_of_cash:
            raise forms.ValidationError(
                'Нельзя использовать оба типа скидки одновременно. Выберите что-то одно.'
            )

        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentStudent
        fields = ['sum', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Применяем стили к полям
        self.fields['sum'].widget.attrs['class'] = form_input_class
        self.fields['sum'].widget.attrs['placeholder'] = 'Введите сумму оплаты'
        self.fields['sum'].label = 'Сумма'
        
        self.fields['comment'].widget = forms.Textarea(attrs={
            'rows': 3,
            'class': form_input_class,
            'placeholder': 'Добавьте комментарий к оплате'
        })
        self.fields['comment'].label = 'Комментарий'
