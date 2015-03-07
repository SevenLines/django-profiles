from django.conf.urls import patterns, include, url
from django.contrib import admin
import profiles.urls

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(profiles.urls))
)
