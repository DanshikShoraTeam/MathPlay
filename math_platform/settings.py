import os
from pathlib import Path

# Корневая папка проекта (папка MathPlay)
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django — используется для шифрования сессий и форм
SECRET_KEY = 'django-insecure-new-forced-reset-key-123'

# Режим разработки: True — подробные ошибки, False — продакшн
DEBUG = True

# Разрешённые хосты — '*' означает любой адрес (для локальной сети)
ALLOWED_HOSTS = ['*']

# Доверенные источники для CSRF-защиты (защита форм от чужих сайтов)
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://*.168.*:*',
    'http://0.0.0.0:8000',
]

# Установленные приложения Django
INSTALLED_APPS = [
    'django.contrib.admin',        # панель администратора
    'django.contrib.auth',         # система авторизации
    'django.contrib.contenttypes', # типы контента
    'django.contrib.sessions',     # сессии пользователей
    'django.contrib.messages',     # flash-сообщения
    'django.contrib.staticfiles',  # статические файлы (CSS, JS, картинки)
    'core',                        # наше приложение
]

# Промежуточные слои (обрабатывают каждый запрос по цепочке)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Файл с корневыми URL-адресами проекта
ROOT_URLCONF = 'math_platform.urls'

# Настройки шаблонов HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # папка с HTML-шаблонами
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

WSGI_APPLICATION = 'math_platform.wsgi.application'

# База данных — SQLite (один файл db.sqlite3 в корне проекта)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей отключена (для простоты на учебном проекте)
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# Путь к статическим файлам (CSS, JS, картинки)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Куда перенаправлять пользователя при входе/выходе
LOGIN_URL           = 'login'
LOGIN_REDIRECT_URL  = 'dashboard'
LOGOUT_REDIRECT_URL = 'homepage'
