# 🚀 SaaSAutomation - Готов к деплою!

## 📁 Структура файлов деплоя

```
SaaSAutomation/
├── deploy-docker.sh              # Скрипт автоматического деплоя
├── docker-compose.yml            # Конфигурация Docker контейнеров
├── Dockerfile                    # Образ для Django приложения
├── nginx-saas-automation.conf    # Конфигурация Nginx
├── core/settings_production.py   # Настройки для продакшена
├── env.production               # Переменные окружения для продакшена
├── env.example                  # Пример переменных окружения
├── DEPLOYMENT.md                # Подробная инструкция по деплою
└── README_DEPLOY.md             # Этот файл
```

## ⚡ Быстрый старт

### 1. На сервере (45.156.22.93):
```bash
# Подключитесь к серверу
ssh kiri@45.156.22.93

# Перейдите в директорию проекта (уже создана через git clone)
cd /home/kiri/SaaSAutomation

# Убедитесь, что все файлы на месте
ls -la
```

### 2. Настройте переменные окружения:
```bash
# Скопируйте файл с настройками
cp env.production .env

# Отредактируйте .env файл
nano .env
```

**Обязательно измените:**
- `SECRET_KEY` - сгенерируйте новый
- `EMAIL_HOST_USER` - ваш email
- `EMAIL_HOST_PASSWORD` - пароль приложения
- `TELEGRAM_BOT_TOKEN` - токен бота

### 3. Запустите деплой:
```bash
# Сделайте скрипт исполняемым
chmod +x deploy-docker.sh

# Запустите деплой
./deploy-docker.sh
```

## 🔧 Что делает скрипт деплоя

1. **Проверяет окружение** - убеждается, что вы на сервере
2. **Останавливает старые контейнеры** - если они запущены
3. **Создает необходимые папки** - logs, staticfiles, media
4. **Собирает Docker образы** - web и db контейнеры
5. **Запускает контейнеры** - в фоновом режиме
6. **Применяет миграции** - создает таблицы в БД
7. **Создает суперпользователя** - admin@saas-automation.com / admin123
8. **Настраивает Nginx** - копирует конфигурацию
9. **Перезагружает Nginx** - применяет настройки

## 🌐 Доступ к приложению

После успешного деплоя:

- **HTTP:** http://45.156.22.93:8000
- **Домен:** https://saas-automation.com (после SSL)
- **Admin:** http://45.156.22.93:8000/admin/
- **API Docs:** http://45.156.22.93:8000/swagger/

**Логин в админку:**
- Email: admin@saas-automation.com
- Пароль: admin123

## 🔒 Настройка SSL (HTTPS)

После деплоя настройте SSL сертификат:

```bash
# Получите SSL сертификат
sudo certbot --nginx -d saas-automation.com -d www.saas-automation.com

# Автоматическое обновление
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Мониторинг

### Проверка статуса:
```bash
# Статус контейнеров
sudo docker-compose ps

# Логи приложения
sudo docker-compose logs -f web

# Логи nginx
sudo tail -f /var/log/nginx/saas-automation.com.access.log
```

### Управление:
```bash
# Остановка
sudo docker-compose down

# Запуск
sudo docker-compose up -d

# Перезапуск
sudo docker-compose restart web
```

## 🛠️ Обновление проекта

```bash
# Остановка контейнеров
sudo docker-compose down

# Обновление кода
git pull origin main

# Пересборка и запуск
sudo docker-compose build
sudo docker-compose up -d

# Применение миграций
sudo docker-compose exec web python manage.py migrate --settings=core.settings_production
```

## 🚨 Устранение неполадок

### Контейнер не запускается:
```bash
sudo docker-compose logs web
sudo docker-compose restart web
```

### Проблемы с базой данных:
```bash
sudo docker-compose exec db psql -U saas_automation -d saas_automation_db
```

### Проблемы с nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 📋 Технические детали

- **Django:** 4.2.18 (LTS)
- **Python:** 3.12
- **PostgreSQL:** 17-alpine
- **Nginx:** Reverse proxy
- **Gunicorn:** WSGI server
- **Docker:** Контейнеризация

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo docker-compose logs -f web`
2. Проверьте статус: `sudo docker-compose ps`
3. Проверьте nginx: `sudo nginx -t`
4. Проверьте порты: `sudo netstat -tlnp | grep :8001`

---

**🎉 Проект готов к деплою! Удачи!**
