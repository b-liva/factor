from .base import *  # noqa
from .base import env

sys.path.insert(0, os.environ.get('ROOT_PATH', '/app/'))
# SECRET_KEY = get_secret_setting('SECRET_KEY_PRODUCTION')
SECRET_KEY = set_secret_key(
    os.environ['DJANGO_SETTINGS_MODULE'],
    'SECRET_KEY_PRODUCTION'
)

# DEBUG = True
# ALLOWED_HOSTS = ['crm.jemcomotor.ir', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}
PORT = os.environ.get('DB_PORT', None)
if PORT:
    DATABASES['default']['PORT'] = PORT
