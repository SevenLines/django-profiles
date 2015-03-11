import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.text import slugify


class ProfileBase(models.Model):
    """
    base abstract model, storing common profile info
    """
    text = models.TextField(default='')
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="", editable=False)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()

        # For automatic slug generation.
        if self.name:
            self.slug = slugify(self.name)[:50]
        else:
            self.slug = unicode(self.pk)
        return super(ProfileBase, self).save(*args, **kwargs)


# Create your models here.
class Profile(ProfileBase):
    @staticmethod
    def list_accessed_by(user):
        """
        :param user:
        :return: profiles which can be accessed by user
        """
        profiles_for_user = ProfilePasskeys.objects.filter(user_id=user.id).values("profile_id").distinct()
        profiles_with_passkeys = ProfilePasskeys.objects.values("profile_id").distinct()
        profiles_without_passkeys = Profile.objects.exclude(pk__in=profiles_with_passkeys).values("id")
        if user.is_superuser:
            return Profile.objects.all()
        if hasattr(user, 'is_admin') and user.is_admin:
            return Profile.objects.filter(Q(pk__in=profiles_for_user) | Q(pk__in=profiles_without_passkeys)) \
                   | user.profile.profiles.all()
        else:
            return Profile.objects.filter(Q(pk__in=profiles_for_user) | Q(pk__in=profiles_without_passkeys))

    def can_be_accessed(self, passkey, user):
        """
        :return: True if user can access profile using provided passkey
        """
        return ProfilePasskeys.objects.filter(passkey=passkey, user=user, profile=self).count() > 0


class ProfilePasskeys(models.Model):
    profile = models.ForeignKey(Profile)
    user = models.ForeignKey(User)
    passkey = models.CharField(max_length=128)

    class Meta:
        unique_together = ('profile', 'user')


