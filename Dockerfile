# Dockerfile для SaaSAutomation Django приложения
# Используем Python 3.9 и PostgreSQL

FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gettext \
        curl \
        wget \
        git \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . /app/

# Создаем пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Создаем папки для логов и статических файлов
RUN mkdir -p /app/logs /app/staticfiles /app/media

# Открываем порт 8001 (не 8000!)
EXPOSE 8001

# Команда по умолчанию - запуск на порту 8001
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "3", "--timeout", "120", "core.wsgi:application"]
