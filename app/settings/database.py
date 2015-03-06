# common DATABASE settings
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import os

from app.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, os.path.join('db', 'db.sqlite3')),
    }
}
