# common DATABASE settings
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import os
import sys

from app.settings import BASE_DIR


if 'test' in sys.argv:
    print('using test database')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, os.path.join('db', 'test_db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, os.path.join('db', 'db.sqlite3')),
        }
    }
