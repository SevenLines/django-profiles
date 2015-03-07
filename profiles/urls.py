from django.conf import settings
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from profiles.api import ProfileResource


v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())

urlpatterns = patterns("profiles.views",
   url(r'(?P<id>\d+)/show/$', "profile.show"),
   url(r'(?P<id>\d+)/update/$', "profile.update"),
   url(r'(?P<id>\d+)/remove/$', "profile.remove"),

   url(r'manager/$', "manager.manager"),
   url(r'manager/profile/(?P<profile_id>\d+)/user/$', "manager.get_profile_users"),
   url(r'manager/user/(?P<user_id>\d+)/profile/$', "manager.get_user_profiles"),
   url(r'manager/profile/(?P<profile_id>\d+)/users/(?P<user_id>\d+)/add', "manager.add_user_to_profile"),
   url(r'manager/profile/(?P<profile_id>\d+)/users/(?P<user_id>\d+)/remove', "manager.remove_user_from_profile"),
   url(r'manager/profile/(?P<profile_id>\d+)/users/(?P<user_id>\d+)/update', "manager.update_user_profile_passkey"),
   url(r'manager/profile/(?P<profile_id>\d+)/check_passkey', "manager.check_passkey"),
   url(r'add/$', "profile.add"),

   url(r'(?P<slug>[\w-]+)/$', "profile.show_by_slug"),
   url(r'$', "profile.index"),
)


# if settings.DEBUG:
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
