import requests
from django.conf import settings


def send_message_telebot(text, chat_id) -> None:
    """
    Отправляет сообщение в Telegram.

    :param text: Текст сообщения
    :param chat_id: ID чата
    """
    api_key = settings.TELEGRAM_BOT_TOKEN

    if settings.DEBUG:
        chat_id = settings.CHAT_ID
    # URL для отправки сообщения
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'

    # Параметры запроса
    params = {'chat_id': chat_id, 'text': text}

    # Отправляем запрос
    requests.post(url, data=params)
