from django.contrib.auth.models import User, AnonymousUser
from django.db import models


def is_admin(user):
    """
    check is user have access to profile management
    """
    if isinstance(user, AnonymousUser):
        return False
    else:
        return user.is_superuser or user.profile.is_admin

# extend user with some helpers methods
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.add_to_class('is_admin', property(is_admin))


class UserProfile(models.Model):
    """
    User model extending
    """
    user = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False, help_text="define is user can assign profiles to users")
    profiles = models.ManyToManyField("Profile",
                                      help_text="the list of profiles which can be changed by user")
