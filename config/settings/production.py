from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Secret Key Generator
if not hasattr(globals(), 'DJANGO_SECRET_KEY'):
    import os
    SECRET_FILE = os.path.join(ROOT_DIR, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except EnvironmentError:
        try:
            from random import choice

            SECRET_KEY = ''.join(
                [choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            with open(SECRET_FILE, 'w') as secret:
                secret.write(SECRET_KEY)
                secret.close()
        except EnvironmentError:
            raise Exception(
                'Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)
else:
    SECRET_KEY = env('DJANGO_SECRET_KEY')


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['www.paparajotesybellotas.com', 'paparajotesybellotas.com'])

# DATABASES
# ------------------------------------------------------------------------------
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'weddb'),
    }
}

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
#SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
#SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
#CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
#SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
#SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
#SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
#SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='Paparajotes Y Bellotas <noreply@paparajotesybellotas.com>'
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Paparajotes Y Bellotas]')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
#ADMIN_URL = env('DJANGO_ADMIN_URL')

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
#INSTALLED_APPS += ['anymail']  # noqa F405
#EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
#ANYMAIL = {
#    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
#    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
#}

# Gunicorn
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['gunicorn']  # noqa F405

# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ['collectfast'] + INSTALLED_APPS  # noqa F405

# Logging Configuration
BASE_LOG_PATH = os.environ.get("PAPYBELL_LOGS_PATH", "/var/log/papybell/")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(module)s.%(funcName)s | %(message)s',
            'datefmt': '%Y%m%d %H:%M:%S',
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'papybell_log.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
        'error_log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'papybell_err.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'papybell_debug.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['debug_log_file'],
            'level': 'DEBUG',
        },
        'paparajotes_y_bellotas': {
            'handlers': ['debug_log_file'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['log_file', 'error_log_file'],
            'level': 'DEBUG',
        },
    }
}

# Your stuff...
# ------------------------------------------------------------------------------
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT", "/var/www/papybell/static")
