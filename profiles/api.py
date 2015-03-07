from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from profiles.models import Profile, ProfilePasskeys

from tastypie.resources import ModelResource


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()


class ProfilePasskeysResource(ModelResource):
    profile = fields.IntegerField(attribute="profile_id")
    user = fields.IntegerField(attribute="user_id")
    class Meta:
        queryset = ProfilePasskeys.objects.all()