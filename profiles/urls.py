from django.conf import settings
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from profiles.api import ProfileResource


v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())

urlpatterns = patterns("profiles.views",
   url(r'(?P<id>\d+)/show/$', "add"),
   url(r'(?P<id>\d+)/update/$', "update"),
   url(r'(?P<id>\d+)/remove/$', "remove"),
   url(r'add/$', "add"),
   url(r'$', "index"),
)


# if settings.DEBUG:
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
