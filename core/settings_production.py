"""
Production settings for SaaSAutomation project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = 'SaaSAutomation'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-production-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SERVER_DOMAIN = os.getenv('SERVER_DOMAIN', 'demo.saas-automation.kz')
SERVER_IP = os.getenv('SERVER_IP', '45.156.22.93')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    SERVER_DOMAIN,
    SERVER_IP,
    'demo.saas-automation.kz',
    'www.demo.saas-automation.kz',
]

INSTALLED_APPS = [
    'jazzmin',
    # default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local application
    'apps.mainapp',
    'apps.base_page',
    'apps.users',
    'apps.students',
    'apps.sales',
    'apps.branches',
    "apps.auth_lms",

    # Приложения для планов
    'apps.plans',

    # Third-party application
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    # Other Libraries
    'django_filters',
    'drf_yasg',
    'corsheaders',
    # 'django_crontab',  # отключено
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'saas_automation_db'),
        'USER': os.getenv('DB_USER', 'saas_automation'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'saas_automation_12345'),
        'HOST': os.getenv('DB_HOST', 'db'),  # Используем имя сервиса из docker-compose
        'PORT': os.getenv('DB_PORT', '5432')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Possibly mutable data
MAX_GROUPS_SIZE = 14
MAX_GROUP_SIZE = 14
WEEKS_BEFORE_START = 8
MIN_STUDENTS_TO_START = 8

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://demo.saas-automation.kz',
    'https://www.demo.saas-automation.kz',
    'http://45.156.22.93',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'rest_framework.authtoken',
    'x-csrftoken',
    'x-requested-with',
]

HTTPS_SERVER_DOMAIN = 'https://' + SERVER_DOMAIN
HTTPS_SERVER_IP = 'https://' + SERVER_IP

CSRF_TRUSTED_ORIGINS = [
    HTTPS_SERVER_DOMAIN,
    HTTPS_SERVER_IP,
    'https://demo.saas-automation.kz',
    'https://www.demo.saas-automation.kz',
    'http://45.156.22.93',
]

# TELEGRAM_BOT_TOKEN (отключено)
# TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# CHAT_ID = os.getenv('CHAT_ID')

# EMAIL_BACKEND
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT', '587')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# CRONJOBS (отключено)
# CRONJOBS = [
#     ('30 3 * * *', 'apps.mainapp.cron.notify_push', f'>> {BASE_DIR}/logs/notify_logs/make_notify.log')
# ]

# JAZZMIN SETTINGS
JAZZMIN_SETTINGS = {
    "site_title": "SaaSAutomation Admin",
    "site_header": "SaaSAutomation Administration",
    "site_brand": "SaaSAutomation",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Добро пожаловать в SaaSAutomation",
    "copyright": "SaaSAutomation",
    "search_model": ["auth.User", "auth.Group"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API", "url": "/swagger/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "API Docs", "url": "/swagger/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "mainapp", "users", "students"],
    "custom_links": {
        "mainapp": [{
            "name": "API Documentation",
            "url": "/swagger/",
            "icon": "fas fa-book",
            "new_window": True,
        }]
    },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "mainapp": "fas fa-home",
        "users": "fas fa-user-friends",
        "students": "fas fa-graduation-cap",
        "sales": "fas fa-chart-line",
        "branches": "fas fa-building",
        "plans": "fas fa-calendar-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

APPEND_SLASH = False

from import_export.formats.base_formats import CSV, XLSX
IMPORT_FORMATS = [CSV, XLSX]

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
