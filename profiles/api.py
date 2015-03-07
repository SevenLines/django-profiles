from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from profiles.models import Profile

from tastypie.resources import ModelResource


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()

