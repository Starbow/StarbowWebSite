"""
Django settings for starbowmodweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from config import *

# Only used when DEBUG = False
ALLOWED_HOSTS = ['162.243.125.126', '.starbowmod.com']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_browserid',
    'starbowmodweb.user',
    'starbowmodweb.ladder',
    'starbowmodweb.site',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # required for admin
    'django_browserid.auth.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django_browserid.context_processors.browserid',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'starbowmodweb.urls'

WSGI_APPLICATION = 'starbowmodweb.apache.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# BrowserID Configuration
AUTH_USER_MODEL = 'user.User'
BROWSERID_CREATE_USER = False
LOGIN_URL = '/user/login_required'
LOGIN_REDIRECT_URL = '/user/home'
LOGIN_REDIRECT_URL_FAILURE = '/user/not_found'
LOGOUT_REDIRECT_URL = '/'
