"""
Django settings for ConfManage project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import djcelery
from celery import  platforms
from kombu import Queue,Exchange

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


''' celery config '''
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER='pickle'
CELERY_ACCEPT_CONTENT = ['pickle','json']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERYD_MAX_TASKS_PER_CHILD = 40
CELERY_TRACK_STARTED = True
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE='Asia/Shanghai'
platforms.C_FORCE_ROOT = True
CELERY_ENABLE_UTC = True

#celery route config
CELERY_IMPORTS = (  "ConfManage.tasks.cron","ConfManage.tasks.sched")
CELERY_QUEUES = (
    Queue('default',Exchange('default'),routing_key='default'),
    Queue('ansible',Exchange('ansible'),routing_key='ansible'),
)
CELERY_ROUTES = {
    'ConfManage.tasks.sql.*':{'queue':'default','routing_key':'default'},
    'ConfManage.tasks.assets.*':{'queue':'default','routing_key':'default'},
    'ConfManage.tasks.cron.*':{'queue':'default','routing_key':'default'},
    'ConfManage.tasks.sched.*':{'queue':'default','routing_key':'default'},
    'ConfManage.tasks.ansible.AnsibleScripts':{'queue':'ansible','routing_key':'ansible'},
    'ConfManage.tasks.ansible.AnsiblePlayBook':{'queue':'ansible','routing_key':'ansible'},
}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'



REDSI_KWARGS_LPUSH = {"host":'127.0.0.1','port':6379,'db':3}
REDSI_LPUSH_POOL = None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x+u%@$*1810rlq0m)$&&v%=y0pod*gaiw428ifb4dc(ul-6f*4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ConfManage',
    'channels',
    'djcelery',
    'baseline',
    'api',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ConfManage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["./ConfManage/templates",
                 "./ConfManage/static"],
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

WSGI_APPLICATION = 'ConfManage.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("192.168.216.130", 6379)],
        },
    },
}

ASGI_APPLICATION = "ConfManage.routing.application"
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'confmanage',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'12345',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    '/ConfManage/static',
)
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


