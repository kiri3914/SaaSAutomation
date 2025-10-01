#!/bin/bash

# Скрипт для деплоя SaaSAutomation на 45.156.22.93
# Запускать НА СЕРВЕРЕ! Использует Docker и существующие nginx/postgres

set -e  # Остановить при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Пути на сервере
SERVER_PATH="/home/kiri/SaaSAutomation"
NGINX_SITES_PATH="/etc/nginx/sites-available"
NGINX_ENABLED_PATH="/etc/nginx/sites-enabled"

log "Начинаем деплой SaaSAutomation с Docker на сервере..."

# Проверка, что мы на сервере
if [[ ! -d "$SERVER_PATH" ]]; then
    error "Этот скрипт нужно запускать на сервере в директории $SERVER_PATH"
    error "Подключитесь к серверу: ssh kiri@45.156.22.93"
    exit 1
fi

# Переход в директорию проекта
cd $SERVER_PATH

# Проверка наличия .env файла
if [[ ! -f ".env" ]]; then
    error "Файл .env не найден. Скопируйте env.example в .env и настройте переменные"
    exit 1
fi

# Остановка существующих контейнеров
log "Останавливаем существующие контейнеры..."
sudo docker compose down 2>/dev/null || true

# Создание папок
log "Создаем необходимые папки..."
mkdir -p logs static media
chmod 777 logs static media

# Получаем UID пользователя appuser из контейнера
log "Настраиваем права доступа для логов..."
CONTAINER_UID=$(sudo docker run --rm python:3.12-slim id -u appuser 2>/dev/null || echo "1000")
CONTAINER_GID=$(sudo docker run --rm python:3.12-slim id -g appuser 2>/dev/null || echo "1000")

# Устанавливаем правильного владельца для папок
sudo chown -R $CONTAINER_UID:$CONTAINER_GID logs static media

# Сборка и запуск контейнера
log "Собираем и запускаем Docker контейнер..."
sudo docker compose build
sudo docker compose up -d

# Ждем запуска контейнера
log "Ждем запуска контейнера..."
sleep 10

# Проверяем, что контейнер запустился
log "Проверяем статус контейнеров..."
for i in {1..30}; do
    if sudo docker compose ps | grep -q "saas_automation_web.*Up"; then
        log "Контейнер web запущен успешно"
        break
    else
        log "Ожидаем запуска контейнера... ($i/30)"
        sleep 2
    fi
done

# Дополнительная проверка
if ! sudo docker compose ps | grep -q "saas_automation_web.*Up"; then
    error "Контейнер web не запустился. Проверьте логи:"
    sudo docker compose logs web
    exit 1
fi

# Ждем готовности базы данных
log "Ждем готовности базы данных..."
for i in {1..20}; do
    if sudo docker compose exec web python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; then
        log "База данных готова"
        break
    else
        log "Ожидаем готовности базы данных... ($i/20)"
        sleep 3
    fi
done

# Исправляем права на папки после запуска контейнера
log "Исправляем права доступа после запуска контейнера..."
sudo chown -R $CONTAINER_UID:$CONTAINER_GID logs static media
sudo chmod -R 755 logs static media

# Создание миграций для всех приложений
log "Создаем миграции для всех приложений..."
sudo docker compose exec web python manage.py makemigrations --settings=core.settings_production

# Применение миграций
log "Применяем миграции базы данных..."
sudo docker compose exec web python manage.py migrate --settings=core.settings_production

# Сбор статических файлов
# log "Собираем статические файлы..."
# sudo docker compose exec web python manage.py collectstatic --noinput --settings=core.settings_production

# Создание суперпользователя (если не существует)
log "Проверяем суперпользователя..."
sudo docker compose exec web python manage.py shell --settings=core.settings_production << 'PYTHON_EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Создаем суперпользователя...")
    User.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@saas-automation.com'
    )
    print("Суперпользователь создан: admin / admin123")
else:
    print("Суперпользователь уже существует")
PYTHON_EOF

# Проверка конфигурации
log "Проверяем конфигурацию Django..."
sudo docker compose exec web python manage.py check --settings=core.settings_production

# Настройка nginx
log "Настраиваем nginx..."
sudo cp nginx-saas-automation.conf ${NGINX_SITES_PATH}/saas-automation.com
sudo ln -sf ${NGINX_SITES_PATH}/saas-automation.com ${NGINX_ENABLED_PATH}/

# Проверка конфигурации nginx
log "Проверяем конфигурацию nginx..."
sudo nginx -t

# Перезагрузка nginx
log "Перезагружаем nginx..."
sudo systemctl reload nginx

# Проверка статуса контейнера
log "Проверяем статус контейнера..."
sudo docker compose ps

success "Деплой завершен!"
log "Следующие шаги:"
echo "1. Настройте SSL сертификат:"
echo "   sudo certbot --nginx -d saas-automation.com"
echo ""
echo "2. Проверьте работу сайта:"
echo "   http://45.156.22.93:8000"
echo "   https://saas-automation.com (после SSL)"
echo ""
echo "3. Проверьте контейнер:"
echo "   sudo docker compose ps"
echo "   sudo docker compose logs -f web"