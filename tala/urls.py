from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")
urlpatterns = patterns(
    '',
    (r'^accounts/', include('djangowind.urls')),
    (r'^$', 'tala.main.views.index'),
    (r'^room/(?P<room_id>\d+)/$', 'tala.main.views.room'),
    (r'^room/(?P<room_id>\d+)/archive/$', 'tala.main.views.room_archive'),
    (r'^room/(?P<room_id>\d+)/archive/(?P<date>\d{4}\-\d+\-\d+)/$',
     'tala.main.views.room_archive_date'),
    (r'^room/(?P<room_id>\d+)/post/$', 'tala.main.views.post_to_room'),
    (r'^room/(?P<room_id>\d+)/fresh_token/$', 'tala.main.views.fresh_token'),
    (r'^admin/', include(admin.site.urls)),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
