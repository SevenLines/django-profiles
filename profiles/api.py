from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication, SessionAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from profiles.models import Profile, ProfilePasskeys

from tastypie.resources import ModelResource


class SuperuserAuthentication(Authentication):
    """
    restricts access for all except superusers
    """

    def is_authenticated(self, request, **kwargs):
        if request.user.is_superuser:
            return True
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
        authentication = SuperuserAuthentication()


class UserResource(ModelResource):
    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(is_superuser=False, is_active=True)

    class Meta:
        queryset = User.objects.all()
        authentication = SuperuserAuthentication()


class ProfilePasskeysResource(ModelResource):
    profile = fields.IntegerField(attribute="profile_id")
    user = fields.IntegerField(attribute="user_id")

    class Meta:
        queryset = ProfilePasskeys.objects.all()
        authentication = SuperuserAuthentication()