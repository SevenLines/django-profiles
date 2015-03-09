import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db import models
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
        if user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(pk__in=ProfilePasskeys.objects.filter(user_id=user.pk).values("profile_id"))

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


