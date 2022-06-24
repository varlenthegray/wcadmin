from wcadmin.settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['wcadev.innovated.tech', 'localhost', '127.0.0.1']

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CSRF_TRUSTED_ORIGINS = ['https://wcadev.innovated.tech']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CONN_MAX_AGE = 20

DATABASES = {
    'default': {
        'HOST': os.environ.get('DB_HOST'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'USER': os.environ.get('DB_USERNAME'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
    }
}
