import datetime
from django.contrib.auth.hashers import make_password, check_password
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
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        return super(ProfileBase, self).save(*args, **kwargs)


# class ProfilePasswords(ProfileBase):
# """
#     model for storing associated with
#     """
#     profile = models.ForeignKey('Profile')
#     passkey = models.CharField(max_length=128)
#
#     def set_passkey(self, raw_passkey):
#         self.passkey = make_password(raw_passkey)
#
#     def check_password(self, raw_passkey):
#         """
#         Returns a boolean of whether the raw_password was correct. Handles
#         hashing formats behind the scenes.
#         """
#
#         def setter(raw_passkey):
#             self.set_password(raw_passkey)
#             self.save(update_fields=["passkey"])
#
#         return check_password(raw_passkey, self.passkey, setter)


# Create your models here.
class Profile(ProfileBase):
    pass
