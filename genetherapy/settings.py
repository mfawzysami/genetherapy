"""
Django settings for genetherapy project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=m@$9yy9chil7u#npl!kg!d!$gj+#f_#fg0#&7rb5d!rc&)!q5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'widget_tweaks',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'genetherapy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'genetherapy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'genetherapy',
        'HOST' :  'localhost',
        'USER' : 'root',
        'PASSWORD' : 'snouto',
        'PORT' : '3306'
    },
    'mongodb': {
        "name": "genetherapy",
        "host": "localhost",
        "tz_aware": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
AUTH_USER_MODEL = 'users.User'
USERS_VERIFY_EMAIL = False
USERS_AUTO_LOGIN_ON_ACTIVATION = True
USERS_SUPERUSER_EMAIL = 'sgp.project.test@gmail.com'
USERS_SUPERUSER_PASSWORD = '0106231078'

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='sgp.project.test@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='0106231078')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='sgp.project.test@gmail.com')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=config('EMAIL_USE_TLS',default=1)

LOGIN_REDIRECT_URL="/"
LOGOUT_REDIRECT_URL = "/"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



BASE_COMMON_URL="http://localhost:8000"
BASE_COMMON_PATH="/"
CELERY_BROKER_URL=config('CELERY_BROKER_URL',default='amqp://guest:guest@localhost:5672//')
CELERY_ENABLE_UTC = True

# Site Manager Email, To Send Job Notifications
SITE_MANAGER_EMAIL = "mfawzy.sami@gmail.com"
INTERNAL_IPS=("127.0.0.1","0.0.0.0")

CELERY_ENV="cyberwatch_Ex"

CELERY_DEFAULT_QUEUE=CELERY_ENV
CELERY_DEFAULT_EXCHANGE=CELERY_ENV
CELERY_DEFAULT_ROUTING_KEY=CELERY_ENV+"_1"
JWT_ALGORITHM = "HS256"


#two Weeks by default
SESSION_COOKIE_AGE = 1209600
RECAPTCHA_VERIFICATION_URL = "https://www.google.com/recaptcha/api/siteverify"
GOOGLE_RECAPTCHA_SECRET_KEY = "6LcSs4UUAAAAAG9_TOQ4ovcu7zxm3XXff3r6NA1e"


### Recaptcha Keys
RECAPTCHA_PUBLIC_KEY = '6LcSs4UUAAAAACAuvbj53uS880v4f_VNrMKLy_Ss'
RECAPTCHA_PRIVATE_KEY = '6LcSs4UUAAAAAG9_TOQ4ovcu7zxm3XXff3r6NA1e'

LOGS_DIR = "/home/snouto/temp"


DASHBOARD_LOGGING = {

    'handler':'file',
    'filename':'cyberwatch.log',
    'settings':{
        'path':os.path.join(LOGS_DIR,'logs'),
        'encoding':'UTF-8'
    }
}