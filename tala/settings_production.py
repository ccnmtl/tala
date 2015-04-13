# flake8: noqa
from settings_shared import *
import sys
import os

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tala',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
        }
}

AWS_STORAGE_BUCKET_NAME = "ccnmtl-tala-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'diabeaters.s3utils.CompressorS3BotoStorage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
DEFAULT_FILE_STORAGE = 'diabeaters.s3utils.MediaRootS3BotoStorage'
MEDIA_URL = S3_URL + '/media/'
COMPRESS_STORAGE = 'diabeaters.s3utils.CompressorS3BotoStorage'
AWS_QUERYSTRING_AUTH = False


COMPRESS_ROOT = "/var/www/tala/tala/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
