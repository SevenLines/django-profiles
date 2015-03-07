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

        self.redirect_to_login_on_get("profiles.views.manager.get_profile_users", pargs=[profile.pk])
        self.redirect_to_login_on_post("profiles.views.manager.get_profile_users", pargs=[profile.pk])

        self.redirect_to_login_on_get("profiles.views.manager.get_user_profiles", pargs=[user.pk])
        self.redirect_to_login_on_post("profiles.views.manager.get_user_profiles", pargs=[user.pk])

        self.redirect_to_login_on_get("profiles.views.manager.add_user_to_profile", pargs=[user.pk, profile.pk])
        self.redirect_to_login_on_post("profiles.views.manager.add_user_to_profile", pargs=[user.pk, profile.pk])

        self.redirect_to_login_on_get("profiles.views.manager.remove_user_from_profile", pargs=[user.pk, profile.pk])
        self.redirect_to_login_on_post("profiles.views.manager.remove_user_from_profile", pargs=[user.pk, profile.pk])

        self.redirect_to_login_on_get("profiles.views.manager.update_user_profile_passkey", pargs=[user.pk, profile.pk])
        self.redirect_to_login_on_post("profiles.views.manager.update_user_profile_passkey", pargs=[user.pk, profile.pk])

        self.redirect_to_login_on_get("profiles.views.manager.check_passkey", pargs=[profile.pk])
        self.redirect_to_login_on_post("profiles.views.manager.check_passkey", pargs=[profile.pk])

