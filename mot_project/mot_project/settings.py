"""
Django settings for interface_experimentation project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mc9e-tp)bkt0+0d^fj&dowldv_vvl5ekdzw#y(cnab5+ne=x-c'
# SECURE_HSTS_SECONDS = 3600*24*30
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'
# CSRF_COOKIE_SECURE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', "127.0.0.1", "flowers-mot.bordeaux.inria.fr", "flowers_mot.bordeaux.inria.fr"]

LOGIN_URL = '/signup_page/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'background_task',
    'interface_app',
    'django_extensions',
    'crispy_forms'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'mot_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mot_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
  'default':{
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': 'mot_db',
   }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
DATE_INPUT_FORMATS = ['%d/%m/%Y','%d-%m-%Y', '%d.%m.%Y']
# USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]


# Emails
# DEFAULT_FROM_EMAIL = 'tenalexander1991@gmail.com'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'tenalexander1991@gmail.com'
# EMAIL_HOST_PASSWORD = '****'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Background tasks
BACKGROUND_TASK_RUN_ASYNC = True # if True, will run the tasks asynchronous. This means the tasks will be processed in parallel (at the same time) instead of processing one by one (one after the other).
# MAX_ATTEMPTS # controls how many times a task will be attempted (default 25)
# MAX_RUN_TIME # maximum possible task run time, after which tasks will be unlocked and tried again (default 3600 seconds)
# BACKGROUND_TASK_ASYNC_THREADS # Specifies number of concurrent threads. Default is multiprocessing.cpu_count().
# BACKGROUND_TASK_PRIORITY_ORDERING # Control the ordering of tasks in the queue. Default is "DESC" (tasks with a higher number are processed first). Choose "ASC" to switch to the “niceness” ordering. A niceness of −20 is the highest priority and 19 is the lowest priority.
