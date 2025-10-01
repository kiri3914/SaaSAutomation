# 🚀 Инструкция по деплою SaaSAutomation

## 📋 Подготовка к деплою

### 1. Подготовка сервера
```bash
# Подключитесь к серверу
ssh kiri@45.156.22.93

# Перейдите в директорию проекта (уже создана через git clone)
cd /home/kiri/SaaSAutomation

# Убедитесь, что все файлы на месте
ls -la
```

### 2. Установка зависимостей на сервере
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker и Docker Compose
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx

# Добавление пользователя в группу docker
sudo usermod -aG docker kiri

# Перезагрузка для применения изменений
sudo reboot
```

### 3. Проект уже клонирован
```bash
# Проект уже находится в /home/kiri/SaaSAutomation
# Если нужно обновить код:
cd /home/kiri/SaaSAutomation
git pull origin main
```

## 🔧 Настройка проекта

### 1. Настройка переменных окружения
```bash
# Скопируйте файл с настройками продакшена
cp env.production .env

# Отредактируйте .env файл
nano .env
```

**Обязательно измените:**
- `SECRET_KEY` - сгенерируйте новый секретный ключ
- `EMAIL_HOST_USER` - ваш email
- `EMAIL_HOST_PASSWORD` - пароль приложения
- `TELEGRAM_BOT_TOKEN` - токен бота
- `CHAT_ID` - ID чата для уведомлений

### 2. Генерация секретного ключа
```bash
# Сгенерируйте новый секретный ключ
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🐳 Запуск с Docker

### 1. Сборка и запуск контейнеров
```bash
# Сделайте скрипт исполняемым
chmod +x deploy-docker.sh

# Запустите деплой
./deploy-docker.sh
```

### 2. Ручной запуск (если скрипт не работает)
```bash
# Сборка контейнеров
sudo docker-compose build

# Запуск контейнеров
sudo docker-compose up -d

# Проверка статуса
sudo docker-compose ps

# Применение миграций
sudo docker-compose exec web python manage.py migrate --settings=core.settings_production

# Создание суперпользователя
sudo docker-compose exec web python manage.py createsuperuser --settings=core.settings_production

# Сбор статических файлов
sudo docker-compose exec web python manage.py collectstatic --noinput --settings=core.settings_production
```

## 🌐 Настройка Nginx

### 1. Копирование конфигурации
```bash
# Скопируйте конфигурацию nginx
sudo cp nginx-saas-automation.conf /etc/nginx/sites-available/saas-automation.com

# Создайте символическую ссылку
sudo ln -sf /etc/nginx/sites-available/saas-automation.com /etc/nginx/sites-enabled/

# Удалите дефолтную конфигурацию (если есть)
sudo rm -f /etc/nginx/sites-enabled/default
```

### 2. Проверка и перезагрузка nginx
```bash
# Проверка конфигурации
sudo nginx -t

# Перезагрузка nginx
sudo systemctl reload nginx

# Проверка статуса
sudo systemctl status nginx
```

## 🔒 Настройка SSL (HTTPS)

### 1. Получение SSL сертификата
```bash
# Получение сертификата Let's Encrypt
sudo certbot --nginx -d saas-automation.com -d www.saas-automation.com

# Автоматическое обновление сертификата
sudo crontab -e
# Добавьте строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## ✅ Проверка деплоя

### 1. Проверка работы сайта
```bash
# Проверка HTTP
curl http://45.156.22.93:8000

# Проверка через браузер
# http://45.156.22.93:8000
# https://saas-automation.com (после SSL)
```

### 2. Проверка контейнеров
```bash
# Статус контейнеров
sudo docker-compose ps

# Логи приложения
sudo docker-compose logs -f web

# Логи базы данных
sudo docker-compose logs -f db
```

### 3. Проверка базы данных
```bash
# Подключение к базе данных
sudo docker-compose exec db psql -U saas_automation -d saas_automation_db

# Проверка таблиц
\dt
\q
```

## 🔧 Управление проектом

### 1. Обновление проекта
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

### 2. Резервное копирование
```bash
# Создание бэкапа базы данных
sudo docker-compose exec db pg_dump -U saas_automation saas_automation_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Создание бэкапа медиа файлов
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### 3. Мониторинг
```bash
# Использование ресурсов
sudo docker stats

# Логи nginx
sudo tail -f /var/log/nginx/saas-automation.com.access.log
sudo tail -f /var/log/nginx/saas-automation.com.error.log

# Логи Django
sudo docker-compose logs -f web
```

## 🚨 Устранение неполадок

### 1. Контейнер не запускается
```bash
# Проверка логов
sudo docker-compose logs web

# Проверка конфигурации
sudo docker-compose config

# Перезапуск контейнера
sudo docker-compose restart web
```

### 2. Проблемы с базой данных
```bash
# Проверка подключения к БД
sudo docker-compose exec web python manage.py dbshell --settings=core.settings_production

# Сброс миграций (ОСТОРОЖНО!)
sudo docker-compose exec web python manage.py migrate --fake-initial --settings=core.settings_production
```

### 3. Проблемы с nginx
```bash
# Проверка конфигурации
sudo nginx -t

# Перезапуск nginx
sudo systemctl restart nginx

# Проверка статуса
sudo systemctl status nginx
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo docker-compose logs -f web`
2. Проверьте статус контейнеров: `sudo docker-compose ps`
3. Проверьте конфигурацию nginx: `sudo nginx -t`
4. Проверьте доступность портов: `sudo netstat -tlnp | grep :8000`
