# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'super_secret_key!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'NAME': 'starbow_website',
        'USER': 'root',
        'PASSWORD': '',
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'NAME': 'mybb',
        'USER': 'root',
        'PASSWORD': '',
    }
}

# Static files
# https://docs.djangoproject.com/en/1.6/howto/static-files/#deployment
MEDIA_ROOT = BASE_DIR+"/media/"
STATIC_ROOT = BASE_DIR+"/static/"

# This is used by BROWSERID to verify login requests. Must match running domain
SITE_URL = 'http://localhost:8000'

# The path to the mybb bridge script. Set to None if you don't have the forum installed
MYBB_BRIDGE_PATH = '/var/www/forum/bridge.php'

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django_browserid': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'starbowmodweb': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}

