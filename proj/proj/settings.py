from pathlib import Path
from dotenv import load_dotenv
from os import path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load `.env` file variables
if path.exists(dotenv_path := BASE_DIR.parent / '.env'):
    load_dotenv(dotenv_path)

# Development settings
SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
DEBUG = eval(os.getenv('DEBUG', 'True'))

ALLOWED_HOSTS = (
    '127.0.0.1',
    'localhost'
)

# Application definition
INSTALLED_APPS = (
    'users.apps.UsersConfig',
    'home.apps.HomeConfig',
    'article.apps.ArticleConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "crispy_bootstrap5",
    'markitup',
    'crispy_forms',
    'django_cleanup.apps.CleanupConfig',
    'sorl.thumbnail',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proj.urls'

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

WSGI_APPLICATION = 'proj.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'

# SMTP
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'pwd.reset@yandex.ru'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PWD')

# Crispy
CRISPY_TEMPCRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
LATE_PACK = 'bootstrap5'

# MarkitUp
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown'
