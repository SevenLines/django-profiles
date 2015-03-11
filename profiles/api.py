from django.contrib.auth.models import User, AnonymousUser
from tastypie import fields
from tastypie.authentication import BasicAuthentication, SessionAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from profiles.models import Profile, ProfilePasskeys

from tastypie.resources import ModelResource
from profiles.models.user_profile import UserProfile


class SuperuserAuthentication(Authentication):
    """
    restricts access for all except admins
    """

    def is_authenticated(self, request, **kwargs):
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username


class ProfileResource(ModelResource):

    def get_object_list(self, request):
        query = super(ProfileResource, self).get_object_list(request)
        if not request.user.is_superuser:
            # get list of profiles that can be managed by this user
            allowed_profiles = request.user.profile.profiles.values("id")
            query = query.filter(id__in=allowed_profiles)
        return query

    class Meta:
        queryset = Profile.objects.all()
        authentication = SuperuserAuthentication()


class UserResource(ModelResource):
    """
    api resource returns info about profile
    excludes superusers and unactive users
    """
    class Meta:
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        queryset = User.objects.filter(is_superuser=False, is_active=True)
        authentication = SuperuserAuthentication()


class AllowedProfileResource(ModelResource):
    """
    api resource helper for UserProfileResource, returns only id of profiles
    """
    class Meta:
        excludes = ['created', 'modified', 'name', 'slug', 'text']
        queryset = Profile.objects.all()
        authentication = SuperuserAuthentication()


class UserProfileResource(ModelResource):
    """
    api resource returning all sensitive info about profile
    excludes superusers, request  user, and unactive users
    """
    user = fields.ToOneField(UserResource, 'user', full=True)
    profiles = fields.ToManyField(AllowedProfileResource, "profiles", full=True)

    def get_object_list(self, request):
        query = super(UserProfileResource, self).get_object_list(request)

        # exclude self
        query = query.exclude(user=request.user)
        return query

    class Meta:
        queryset = UserProfile.objects.filter(user__is_superuser=False, user__is_active=True)
        authentication = SuperuserAuthentication()


class ProfilePasskeysResource(ModelResource):
    profile = fields.IntegerField(attribute="profile_id")
    user = fields.IntegerField(attribute="user_id")

    class Meta:
        queryset = ProfilePasskeys.objects.all()
        authentication = SuperuserAuthentication()