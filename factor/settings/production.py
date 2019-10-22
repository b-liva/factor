from .base import *  # noqa
from .base import env
# SECRET_KEY = get_secret_setting('SECRET_KEY_PRODUCTION')
SECRET_KEY = set_secret_key(
    os.environ['DJANGO_SETTINGS_MODULE'],
    'SECRET_KEY_PRODUCTION'
)

print('secret key: ', SECRET_KEY)
DEBUG = True
ALLOWED_HOSTS = ['crm.jemcomotor.ir', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jcrm_production',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}