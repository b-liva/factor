"""
Django settings for factor project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import environ

ROOT_DIR = (
    environ.Path(__file__) - 2
)  # (nikan/config/settings/base.py - 3 = nikan/)
# APPS_DIR = ROOT_DIR.path("factor")
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))
DEBUG = env.bool("DJANGO_DEBUG", False)

import os

import sys

from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, '../../templates')
FRONTEND_DIR = os.path.join(BASE_DIR, '../../frontend')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'wf$gn46*y4((^9gsj8_4j=%i=40v2dpuyypf56xww72aj40b5='
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '192.168.1.4']

# Application definition
SITE_ID = 1

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Ticket
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    'django_filters',
    'import_export',
    'rest_framework',
    'rest_framework.authtoken',
    'django_jalali',
    'django_cleanup.apps.CleanupConfig',
    'webpack_loader',
    'pytest_django',
]

LOCAL_APPS = [
    # Your stuff: custom apps go here
    'accounts.apps.AccountsConfig',
    'request.apps.RequestConfig',
    'api.apps.ApiConfig',
    'tender.apps.TenderConfig',
    'customer.apps.CustomerConfig',
    'fund.apps.FundConfig',
    'req_track.apps.ReqTrackConfig',
    'spec_communications.apps.SpecCommunicationsConfig',
    'pricedb.apps.PricedbConfig',
    'motordb.apps.MotordbConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'accounts.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = reverse_lazy('account_login')

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_ROOT = os.path.join(BASE_DIR, '../../static')

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')
ROOT_URLCONF = 'factor.urls'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        # "DIRS": [str(APPS_DIR.path("templates"))],
        'DIRS': [
            os.path.join(BASE_DIR, 'request/../../request/templates'),
            os.path.join(BASE_DIR, 'reportbugs/templates'),
            os.path.join(BASE_DIR, 'api/v1/../../api/v1/templates'),
            os.path.join(BASE_DIR, '../../templates')
        ],
        'APP_DIRS': True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
        },
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
# CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
# FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""basir""", "basir@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': DEBUG,
        'BUNDLE_DIR_NAME': '/bundles/',  # must end with slash
        'STATS_FILE': os.path.join(FRONTEND_DIR, 'webpack-stats.json'),
    }
}

WSGI_APPLICATION = 'factor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'jemco$jemcodb',
#         'USER': 'jemco',
#         'PASSWORD': 'Pythonpass21',
#         'HOST': 'jemco.mysql.pythonanywhere-services.com',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         },
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newfromlive',
        'USER': 'root',
        'PASSWORD': '',
        # 'PASSWORD': 'livapass',
        'HOST': 'localhost',
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        # },
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../../test_database.sqlite3'),
        },
    }
}
if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 20,
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

ACCOUNT_FORMS = {
    'login': 'accounts.forms.CustomLoginForm',
    'signup': 'accounts.forms.CustomSignForm',
    'change_password': 'accounts.forms.CustomChangePasswordForm',
    'reset_password': 'accounts.forms.CustomerResetPasswordForm',
    'set_password': 'accounts.forms.CustomerResetPasswordForm',
    'reset_password_from_key': 'accounts.forms.CustomResetPasswordKeyForm',
}

ACCOUNT_SESSION_REMEMBER = False
SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_LOGOUT_REDIRECT_URL = 'accounts/login'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.pop3.EmailBackend'

# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'mail.vbstech.ir'
# EMAIL_PORT = 25
# # EMAIL_PORT = 587
# # EMAIL_PORT = 465
# DEFAULT_FROM_EMAIL = 'sales@vbstech.ir'
# EMAIL_HOST_USER = 'sales@vbstech.ir'
# EMAIL_HOST_PASSWORD = 'newpassword'
EMAIL_HOST = 'mail.vbstech.ir'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'crm@jemcomotor.ir'
EMAIL_HOST_USER = 'crm@jemcomotor.ir'
EMAIL_HOST_PASSWORD = 'jcrmpasswd'

SITE_NAME = DEFAULT_FROM_EMAIL
IMPORT_EXPORT_USE_TRANSACTIONS = True

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda x: False,
# }
