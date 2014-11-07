import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/tala/tala/ve/lib/python2.7/site-packages')
sys.path.append('/var/www/tala/tala/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tala.settings_staging'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
