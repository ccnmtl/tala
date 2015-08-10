# Django settings for tala project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tala',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/tala/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'djangowind.context.context_processor',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'tala.urls'

TEMPLATE_DIRS = (
    "/var/www/tala/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'tala.main',
    'django_jenkins',
    'waffle',
    'smoketest',
    'django_markwhat',
]

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'tala'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

SENTRY_REMOTE_URL = 'http://sentry.ccnmtl.columbia.edu/sentry/store/'
# remember to set the SENTRY_KEY in a local_settings.py
# as documented in the wiki
SENTRY_SITE = 'tala'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['tala.main', ]

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[tala] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "tala@ccnmtl.columbia.edu"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

STATICMEDIA_MOUNTS = (
    ('/static', 'sitemedia'),
)

STATIC_ROOT = "/tmp/tala/static"
STATICFILES_DIRS = ("media/",)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

# WIND settings

AUTHENTICATION_BACKENDS = (
    'djangowind.auth.SAMLAuthBackend',
    'django.contrib.auth.backends.ModelBackend',)
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = [
    'djangowind.auth.AffilGroupMapper',
    'djangowind.auth.StaffMapper',
    'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = [
    'anp8', 'jb2410', 'zm4', 'egr2107', 'sld2131',
    'amm8', 'mar227']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

WINDSOCK_BROKER_URL = "tcp://localhost:5555"
ZMQ_APPNAME = "tala"
WINDSOCK_SECRET = "6f1d916c-7761-4874-8d5b-8f8f93d20bf2"
WINDSOCK_WEBSOCKETS_BASE = "ws://localhost:5050/socket/"
ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
