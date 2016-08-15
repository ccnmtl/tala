import django.views.static
import os.path

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from tala.main.views import (
    index, room, room_archive, room_archive_date, post_to_room,
    fresh_token
)

admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")
urlpatterns = [
    url(r'^accounts/', include('djangowind.urls')),
    url(r'^$', index),
    url(r'^room/(?P<room_id>\d+)/$', room),
    url(r'^room/(?P<room_id>\d+)/archive/$', room_archive),
    url(r'^room/(?P<room_id>\d+)/archive/(?P<date>\d{4}\-\d+\-\d+)/$',
        room_archive_date),
    url(r'^room/(?P<room_id>\d+)/post/$', post_to_room),
    url(r'^room/(?P<room_id>\d+)/fresh_token/$', fresh_token),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^site_media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': site_media_root}),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
