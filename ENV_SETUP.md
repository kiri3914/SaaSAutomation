# 🔧 Настройка переменных окружения для SaaSAutomation

## 📋 Быстрый старт

1. **Скопируйте файл примера:**
   ```bash
   cp env.example .env
   ```

2. **Отредактируйте `.env` файл** и заполните реальными значениями

3. **Запустите проект:**
   ```bash
   source venv/bin/activate.fish
   python manage.py runserver
   ```

## 🔑 Обязательные переменные

### Для разработки:
```env
DEBUG=1
SECRET_KEY=your-secret-key-here
SERVER_DOMAIN=localhost
SERVER_IP=127.0.0.1
```

### Для продакшена:
```env
DEBUG=0
SECRET_KEY=your-production-secret-key
SERVER_DOMAIN=yourdomain.com
SERVER_IP=your-server-ip
```

## 🗄️ Настройка базы данных

### SQLite (по умолчанию для разработки):
Никаких дополнительных настроек не требуется.

### PostgreSQL (для продакшена):
```env
DB_NAME=saasautomation_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## 📧 Настройка email

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## 🤖 Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен и добавьте в `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   CHAT_ID=your-chat-id
   ```

## 🔒 Безопасность

- ✅ Никогда не коммитьте `.env` файл в git
- ✅ Используйте разные `.env` файлы для разных окружений
- ✅ Регулярно обновляйте секретные ключи
- ✅ Используйте сильные пароли для продакшена
- ✅ Настройте HTTPS в продакшене

## 🚀 Дополнительные настройки

См. файл `env.example` для полного списка всех доступных переменных окружения.

## ❓ Помощь

Если у вас возникли проблемы с настройкой, проверьте:
1. Правильность синтаксиса в `.env` файле
2. Наличие всех обязательных переменных
3. Корректность значений (особенно для внешних сервисов)
