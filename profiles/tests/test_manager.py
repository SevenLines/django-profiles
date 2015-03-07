import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from profiles.models import Profile, ProfilePasskeys
from app.utils import TestCaseEx


class TestManagerViews(TestCaseEx):
    def test_guest_cant_work_with_manager_views(self):
        profile = Profile.objects.create(name=u"name")
        user = User.objects.first()

        ProfilePasskeys.objects.all().delete()
        ProfilePasskeys.objects.create(profile=profile, user=user, passkey='12345')

        self.redirect_to_login_on_get("profiles.views.manager.manager")
        self.redirect_to_login_on_post("profiles.views.manager.manager")

    @TestCaseEx.login
    def test_simple_user_cant_work_with_manager_view(self):
        profile = Profile.objects.create(name=u"name")
        user = User.objects.first()

        ProfilePasskeys.objects.all().delete()
        ProfilePasskeys.objects.create(profile=profile, user=user, passkey='12345')

        self.redirect_to_login_on_get("profiles.views.manager.manager")
        self.redirect_to_login_on_post("profiles.views.manager.manager")

    @TestCaseEx.superuser
    def test_superuser_can_work_with_manager_view(self):
        profile = Profile.objects.create(name=u"name")
        user = User.objects.first()

        ProfilePasskeys.objects.all().delete()
        ProfilePasskeys.objects.create(profile=profile, user=user, passkey='12345')

        self.can_get("profiles.views.manager.manager")


    def test_guest_cant_update_profile_passkeys(self):
        self.redirect_to_login_on_get("profiles.views.manager.update_profile_passkeys")
        self.redirect_to_login_on_post("profiles.views.manager.update_profile_passkeys")

    @TestCaseEx.login
    def test_simple_user_cant_update_profile_passkeys(self):
        self.redirect_to_login_on_get("profiles.views.manager.update_profile_passkeys")
        self.redirect_to_login_on_post("profiles.views.manager.update_profile_passkeys")

    @TestCaseEx.superuser
    def test_update_profile_passkeys_should_update_existing_passkeys(self):
        ProfilePasskeys.objects.all().delete()

        profile = Profile.objects.create(name=u"name")
        user = User.objects.first()
        passkey = ProfilePasskeys.objects.create(profile=profile, user=user, passkey=u'12345')

        new_values = {
            "profile_passkeys": json.dumps([
                {"profile": profile.pk, "user": user.pk, "passkey": u'54321'}
            ])
        }

        self.can_post("profiles.views.manager.update_profile_passkeys", params=new_values)

        passkey = ProfilePasskeys.objects.get(pk=passkey.pk)

        self.assertEqual(passkey.passkey, u'54321')

    @TestCaseEx.superuser
    def test_update_profile_passkeys_can_create_new_passkey_triple(self):
        ProfilePasskeys.objects.all().delete()

        profile = Profile.objects.create(name=u"name")
        user = User.objects.first()

        new_values = {
            "profile_passkeys": json.dumps([
                {"profile": profile.pk, "user": user.pk, "passkey": u'54321'}
            ])
        }

        self.can_post("profiles.views.manager.update_profile_passkeys", params=new_values)

        passkey = ProfilePasskeys.objects.order_by("-pk").first()

        self.assertEqual(passkey.passkey, u'54321')

    @TestCaseEx.superuser
    def test_update_profile_passkeys_can_delete_existing_triples(self):
        ProfilePasskeys.objects.all().delete()

        profile = Profile.objects.create(name=u"name")
        profile2 = Profile.objects.create(name=u"name2")
        user = User.objects.first()
        ProfilePasskeys.objects.create(profile=profile, user=user, passkey=u'12345')
        ProfilePasskeys.objects.create(profile=profile2, user=user, passkey=u'12345')

        new_values = {
            "profile_passkeys": json.dumps([
                {"profile": profile.pk, "user": user.pk, "passkey": u'', u'allowed': False}
            ])
        }

        self.can_post("profiles.views.manager.update_profile_passkeys", params=new_values)

        self.assertEqual(ProfilePasskeys.objects.filter(profile=profile2).count(), 1)
        self.assertEqual(ProfilePasskeys.objects.filter(profile=profile).count(), 0)