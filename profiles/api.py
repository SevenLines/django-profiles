from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from profiles.models import Profile

from tastypie.resources import ModelResource


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()

