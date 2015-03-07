"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Make sure that you create credentials.json file in root directory
try:
    credentials = json.loads(open("credentials.json").read())
except BaseException as e:
    print "You probably forget to create credentials.json (check credentials_sample.json)"
    raise e


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rbt3_6pnv)@ax*%yqd**5i$kc!zn5er%_)lr9pp6&&l81x12&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(credentials.get('DEBUG', 0)) == 1
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = credentials.get("ALLOWED_HOSTS", ['*', ])

from app.settings.apps import *
from app.settings.middleware import *
from app.settings.database import *
from app.settings.dirs import *

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = credentials.get("EMAIL_HOST", 'localhost')
EMAIL_HOST_USER = credentials.get("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = credentials.get("EMAIL_HOST_PASSWORD", '')