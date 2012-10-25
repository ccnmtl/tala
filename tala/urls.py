from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__),"../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/',include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$','django.contrib.auth.views.logout', {'next_page': redirect_after_logout})
if hasattr(settings,'WIND_BASE'):
    auth_urls = (r'^accounts/',include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$','djangowind.views.logout', {'next_page': redirect_after_logout})

urlpatterns = patterns('',
                       # Example:
                       # (r'^tala/', include('tala.foo.urls')),
		       auth_urls,
		       logout_page,
                       (r'^$', 'tala.main.views.index'),
                       (r'^room/(?P<room_id>\d+)/$', 'tala.main.views.room'),
                       (r'^room/(?P<room_id>\d+)/post/$', 'tala.main.views.post_to_room'),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^munin/',include('munin.urls')),
											 (r'^stats/', direct_to_template, {'template': 'stats.html'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) + staticmedia.serve()

