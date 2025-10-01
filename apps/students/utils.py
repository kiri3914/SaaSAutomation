import os   
import base64
import pdfkit
import logging
from django.template.loader import render_to_string
from django.utils import timezone
from django.forms import ValidationError
from django.conf import settings
from urllib.parse import unquote
logger = logging.getLogger(__name__)



def valid_telegram(nik: str) -> str:
    return nik.replace('@', '')


def valid_phone(phone: str) -> None:
    if '+' not in phone:
        raise ValidationError('Введите номер в международном формате')
    for i in phone:
        if i not in '()- +1234567890':
            raise ValidationError(f'Номер не может включать {i}')


def payment_for_current_mount(self) -> int:
    """Вычисление сколько нужно оплатить за текущий месяц"""
    current_mount = self.course.current_month_course                 # Текущий месяц
    sum_one_mount = self.full_payment / self.course.course_duration   # сумма за месяц
    sum_ = sum_one_mount * current_mount - self.payment               # оплата за текущий месяц
    return round(sum_ if sum_ > 0 else 0)


def validate_positive(value):
    if value <= 0:
        raise ValidationError("Значение должно быть положительным и больше нуля.")




def format_number(value):
    return f"{value:,.2f}".replace(",", " ")

def generate_receipt_number(payment):
    return f'{payment.date.strftime("%d%m%y")}{payment.id:06d}'

def convert_image_to_base64(file_path):
    try:
        # Декодируем URL-кодированное имя файла
        file_path = unquote(file_path)
        # Если file_path — это относительный URL, преобразуем его в абсолютный путь
        if file_path.startswith('/media/'):
            # Удаляем '/media/' из начала пути, чтобы избежать дублирования
            relative_path = file_path.lstrip('/media/')
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        logger.debug(f"Attempting to open file: {file_path}")
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return None

def prepare_context(payment):
    logo_base64 = convert_image_to_base64('static/img/logo.png')
    if payment.student.course.branch.stamp:
        stamp_base64 = convert_image_to_base64(payment.student.course.branch.stamp.url)
    else:
        stamp_base64 = None
    date_time = timezone.localtime(payment.date)
    course_name = payment.student.course.title
    student_name = payment.student.full_name
    amount = f"{format_number(payment.sum)} {payment.student.course.branch.currency}"
    receipt_number = generate_receipt_number(payment)
    city = payment.student.course.branch.city
    comment = payment.comment
    organization = payment.student.course.branch.organization
    bik = payment.student.course.branch.bik
    bin = payment.student.course.branch.bin
    account = payment.student.course.branch.account
    director_name = payment.student.course.branch.director_name

    return {
        'logo_base64': logo_base64,
        'stamp_base64': stamp_base64,
        'course_name': course_name,
        'student_name': student_name,
        'amount': amount,
        'receipt_number': receipt_number,
        'comment': comment,
        'city': city,
        'organization': organization,
        'bik': bik,
        'bin': bin,
        'account': account,
        'datetime': date_time.strftime("%H:%M:%S %d.%m.%Y"),
        'payer_name': student_name,
        'payment_method': payment.comment,
        'director_name': director_name
    }

def generate_pdf(payment):
    context = prepare_context(payment)
    try:
        html = render_to_string('students/receipt.html', context)
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': True,
            'dpi': 300,
            'image-quality': 200, # качество изображения
            'margin-top': '10mm',  # Дополнительные отступы для предотвращения наложения
            'margin-bottom': '20mm',
            'zoom': 1.0,  # Убедимся, что масштаб не искажает элементы
            'disable-smart-shrinking': None,  # Отключаем сжатие для точного рендеринга
        }
        pdf = pdfkit.from_string(html, False, options=options)
        number = context['receipt_number']
        pdf_path = f'media/receipts/{number}.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        payment.receipt = f'receipts/{number}.pdf'
        payment.save()
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise