"""
With these settings, tests run faster.
"""

from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# secret key from environment variables.
# SECRET_KEY = env(
#     "DJANGO_SECRET_KEY",
#     default="fhzDw68Aq75xg9I3QkpMNd40JYak98wvF1ryJ1Q1hC7oNH7KibU6P4HVyaemkBTY",
# )
# SECRET_KEY = get_secret_setting('SECRET_KEY_TEST')
SECRET_KEY = os.environ['SECRET_KEY_TEST']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

DB_DRIVER = os.environ.get('DB_DRIVER', 'sqlite')
print("db driver: ", DB_DRIVER)
if DB_DRIVER == 'sqlite':

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(ROOT_DIR, 'test_database.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'jcm3'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASS', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'TEST': {
                'NAME': os.environ.get('DB_NAME_TEST', 'test_jtest3'),
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            },
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                # 'init_command': 'ALTER DATABASE <YOUR_DB_NAME> CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci',
            },
        },
    }

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
TEMPLATES[0]["APP_DIRS"] = False

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------
