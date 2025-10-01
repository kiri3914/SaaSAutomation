from datetime import datetime
from django.conf import settings
import subprocess

BASE_DIR = settings.BASE_DIR


def notify_push():
    time = datetime.now().strftime("[%B %d, %Y - %H:%M:%S]")
    command = f'{BASE_DIR}/venv/bin/python {BASE_DIR}/manage.py notify_push'
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        print(f"{time}: Уведомление о старте группы прошло успешно! Вывод команды: {output}")
    except subprocess.CalledProcessError as e:
        print(f"{time}: Уведомление о старте группы не прошло! Код возврата: {e.returncode}. Вывод команды: {e.output}")
