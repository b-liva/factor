from .base import *  # noqa
from .base import env
# SECRET_KEY = get_secret_setting('SECRET_KEY_STAGING')
SECRET_KEY = os.environ['SECRET_KEY_STAGING']

DEBUG = True
ALLOWED_HOSTS = ['www.vbstech.ir', 'localhost', '127.0.0.1']


EMAIL_HOST = 'mail.vbstech.ir'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'crm@jemcomotor.ir'
EMAIL_HOST_USER = 'crm@jemcomotor.ir'
EMAIL_HOST_PASSWORD = 'jcrmpasswd'

SITE_NAME = DEFAULT_FROM_EMAIL
IMPORT_EXPORT_USE_TRANSACTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jcrm_staging',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}
