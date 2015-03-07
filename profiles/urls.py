from django.conf import settings
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from profiles.api import ProfileResource, UserResource, ProfilePasskeysResource


# register api for REST access with tastypie
v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())
v1_api.register(UserResource())
v1_api.register(ProfilePasskeysResource())

urlpatterns = patterns("profiles.views",
   url(r'(?P<id>\d+)/show/$', "profile.show"),
   url(r'(?P<id>\d+)/update/$', "profile.update"),
   url(r'(?P<id>\d+)/remove/$', "profile.remove"),
   url(r'(?P<id>\d+)/enter-passkey/', "profile.provide_passkey"),
   url(r'add/$', "profile.add"),

   url(r'manager/$', "manager.manager"),
   url(r'manager/profile/(?P<profile_id>\d+)/check_passkey', "manager.check_passkey"),
   url(r'manager/update-profile-passkeys/', "manager.update_profile_passkeys"),

   url(r'api/', include(v1_api.urls)),
   url(r'(?P<slug>[\w-]+)/$', "profile.show_by_slug"),
   url(r'$', "profile.index"),
)


# if settings.DEBUG:
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
