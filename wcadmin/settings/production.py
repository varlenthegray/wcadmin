from wcadmin.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
with open('/home/innovated/domains/wcadmin.innovated.tech/public_html/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://wcadmin.innovated.tech']

CSRF_TRUSTED_ORIGINS = ['https://wcadmin.innovated.tech']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CONN_MAX_AGE = 20

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
with open('/home/innovated/domains/wcadmin.innovated.tech/public_html/database.txt') as f:
    DATABASES = {
        'default': {
            'HOST': '',
            'PASSWORD': f.read().strip(),
            'USER': 'innovated',
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wcadmin',
        }
    }
