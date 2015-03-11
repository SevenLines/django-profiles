from django.conf import settings
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from profiles.api import ProfileResource, UserResource, ProfilePasskeysResource, UserProfileResource


# register api for REST access with tastypie
v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(ProfilePasskeysResource())

urlpatterns = patterns("profiles.views",
   url(r'(?P<id>\d+)/show/$', "profile.show"),
   url(r'(?P<id>\d+)/update/$', "profile.update"),
   url(r'(?P<id>\d+)/remove/$', "profile.remove"),
   url(r'(?P<id>\d+)/enter-passkey/', "profile.provide_passkey"),
   url(r'add/$', "profile.add"),

   url(r'manager/update-profile-passkeys/', "manager.update_profile_passkeys"),
   url(r'manager/update-allowed-profiles/', "manager.update_allowed_profiles"),
   url(r'manager/send-passkey-email$', "manager.send_passkey_to_email"),
   url(r'manager/$', "manager.manager"),

   url(r'api/', include(v1_api.urls)),
   url(r'(?P<slug>[\w-]+)/$', "profile.show_by_slug"),
   url(r'$', "profile.index"),
)