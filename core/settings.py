import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = 'Itc service'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5ieo(=y-(4ty-!w(xlpwo40u3938ey4d1)39j2p%oc^jcv@(9*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG')))

SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')
SERVER_IP = os.getenv('SERVER_IP')

ALLOWED_HOSTS = ['127.0.0.1', SERVER_DOMAIN, SERVER_IP]

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
    'django_crontab',
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
#
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('NAME'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
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
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']
else:
    STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Possibly mutable data
# 1. Maximum number of students in a group
MAX_GROUPS_SIZE = 14

# Добавим настройки для групп
MAX_GROUP_SIZE = 14
WEEKS_BEFORE_START = 8  # За сколько недель до старта должны набрать группу
MIN_STUDENTS_TO_START = 8  # Минимальное количество студентов для старта

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'https://127.0.0.1',
    'https://localhost',
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

CSRF_TRUSTED_ORIGINS = [HTTPS_SERVER_DOMAIN, HTTPS_SERVER_IP]

# TELEGRAM_BOT_TOKEN
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# EMAIL_BACKEND
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

CRONJOBS = [
    ('30 3 * * *', 'apps.mainapp.cron.notify_push', f'>> {BASE_DIR}/logs/notify_logs/make_notify.log')
]

JAZZMIN_SETTINGS = {
    "site_title": "Admin Portal",
    "site_header": "My Administration",
    # ... other Jazzmin settings ...
}

JAZZMIN_UI_TWEAKS = {
    "brand_colour": "green",
    "accent": "green",
    "navbar": "navbar-dark",
    # ... other UI tweaks ...
}
APPEND_SLASH=False

from import_export.formats.base_formats import CSV, XLSX
IMPORT_FORMATS = [CSV, XLSX]


LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'