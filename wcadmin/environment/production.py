from wcadmin.settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['admin.wcwater.com', 'localhost', '127.0.0.1']

# noinspection PyUnresolvedReferences
# STATIC_ROOT = '/home/wcadmin/public_html/wcadmin/static/'

CSRF_TRUSTED_ORIGINS = ['https://admin.wcwater.com']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CONN_MAX_AGE = 20

DATABASES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PG_DB_NAME'),
        'USER': os.environ.get('PG_DB_USER'),
        'PASSWORD': os.environ.get('PG_DB_PASSWORD'),
        'HOST': os.environ.get('PG_DB_HOST'),
        'PORT': os.environ.get('PG_DB_PORT'),
    },
}
