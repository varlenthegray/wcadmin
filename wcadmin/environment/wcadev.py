from wcadmin.settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['wcadev.innovated.tech', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://wcadev.innovated.tech']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CONN_MAX_AGE = 20

# DATABASES = {
#     'default': {
#         'HOST': os.environ.get('DB_HOST'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'USER': os.environ.get('DB_USERNAME'),
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ.get('DB_NAME'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PG_DB_NAME'),
        'USER': os.environ.get('PG_DB_USER'),
        'PASSWORD': os.environ.get('PG_DB_PASSWORD'),
        'HOST': os.environ.get('PG_DB_HOST'),
        'PORT': os.environ.get('PG_DB_PORT'),
    }
}
