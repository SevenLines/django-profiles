import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from app.utils import TestCaseEx
from profiles.models import Profile, ProfilePasskeys
from profiles.views.profile import session_passkeys


class TestProfilesViews(TestCaseEx):
    def test_anyone_can_see_index_page(self):
        self.can_get("profiles.views.profile.index")

    def test_if_profile_dont_have_users_anyone_can_see_it(self):
        p = Profile.objects.create()
        self.can_get("profiles.views.profile.show", pargs=[p.pk])

    def test_if_profile_have_associated_users_only_they_can_see_it(self):
        p = Profile.objects.create()
        user = User.objects.create_user("user2", password="123")
        ProfilePasskeys.objects.create(user=user, profile=p, passkey="coolpasskey")

        # guest cant see that profile
        self.redirect_to_login_on_get("profiles.views.profile.show", pargs=[p.pk])

        # associated user cant without provided passkey
        self.client.login(username=user, password="123")
        response = self.redirect_on_get("profiles.views.profile.show", pargs=[p.pk])
        self.assertRedirects(response, reverse("profiles.views.profile.provide_passkey", args=[p.pk]))
        self.client.logout()

        # associated user can with correct passkey
        self.client.login(username=user, password="123")
        session = self.client.session
        session[session_passkeys] = {
            p.id: "coolpasskey"
        }
        session.save()
        self.can_get("profiles.views.profile.show", pargs=[p.pk])

        #user dont need to enter password two times
        self.can_get("profiles.views.profile.show", pargs=[unicode(p.pk)])
        self.client.logout()


    def test_if_profile_have_associated_users_they_should_provide_passkey_to_view_it(self):
        p = Profile.objects.create()
        user = User.objects.create_user("user2", password="123")
        ProfilePasskeys.objects.create(user=user, profile=p)

    @TestCaseEx.superuser
    def test_superuser_can_see_all_profiles(self):
        p = Profile.objects.create()
        user = User.objects.create_user("user3", password="123")
        ProfilePasskeys.objects.create(user=user, profile=p)

        self.can_get("profiles.views.profile.show", pargs=[p.pk])

    def test_guest_cant_add(self):
        self.redirect_on_post("profiles.views.profile.add")
        self.redirect_on_get("profiles.views.profile.add")

    @TestCaseEx.login
    def test_simple_user_cant_add(self):
        self.redirect_on_post("profiles.views.profile.add")
        self.redirect_on_get("profiles.views.profile.add")

    @TestCaseEx.superuser
    def test_adding_should_create_new_profile(self):
        self.can_get("profiles.views.profile.add")  # check that we can get add page

        count_before = Profile.objects.count()
        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.redirect_on_post("profiles.views.profile.add", params)

        self.assertEqual(count_before + 1, Profile.objects.count())
        new_profile = Profile.objects.order_by("-pk").first()
        self.assertEqual(new_profile.text, params['text'])
        self.assertEqual(new_profile.name, params['name'])

        self.assertRedirects(response, reverse("profiles.views.profile.show_by_slug", args=[new_profile.slug]))

    @TestCaseEx.superuser
    def test_adding_with_ajax_should_create_new_profile(self):
        count_before = Profile.objects.count()
        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.can_post("profiles.views.profile.add", params, ajax=True)
        self.assertEqual(count_before + 1, Profile.objects.count())

        data = json.loads(response.content)

        new_profile = Profile.objects.order_by("-pk").first()
        self.assertEqual(data['fields']['text'], params['text'])
        self.assertEqual(int(data['pk']), new_profile.pk)
        self.assertEqual(new_profile.text, params['text'])
        self.assertEqual(data['fields']['name'], params['name'])
        self.assertEqual(new_profile.name, params['name'])

    def test_guest_cant_update(self):
        p = Profile.objects.create(name=u"some_new_name")
        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        self.redirect_on_post("profiles.views.profile.update", pargs=[p.pk], params=params)
        self.redirect_on_get("profiles.views.profile.update", pargs=[p.pk], params=params)

    @TestCaseEx.login
    def test_simple_user_cant_update_without_correct_passkey_in_session(self):
        profile = Profile.objects.create(name=u"some_new_name")

        ProfilePasskeys.objects.all().delete()
        ProfilePasskeys.objects.create(user=self.user, profile=profile, passkey="5678")

        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.redirect_on_post("profiles.views.profile.update", params=params, pargs=[profile.pk, ])
        self.assertRedirects(response, reverse("profiles.views.profile.provide_passkey", args=[profile.pk]))


    @TestCaseEx.login
    def test_simple_user_can_update_with_correct_passkey_in_session(self):
        profile = Profile.objects.create(name=u"some_new_name")
        user = User.objects.create_user("sample_user3", password="12345")

        ProfilePasskeys.objects.all().delete()
        ProfilePasskeys.objects.create(user=self.user, profile=profile, passkey="5678")

        session = self.client.session
        session[session_passkeys] = {
            profile.id: "5678"
        }
        session.save()

        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.can_get("profiles.views.profile.update", params=params, pargs=[profile.pk])

    @TestCaseEx.superuser
    def test_update_should_update_values(self):
        p = Profile.objects.create(name=u"some_new_name")

        self.can_get("profiles.views.profile.update", pargs=[p.pk])  # check that we can get update page

        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.redirect_on_post("profiles.views.profile.update", params=params, pargs=[p.pk])

        p = Profile.objects.get(pk=p.pk)
        self.assertRedirects(response, reverse("profiles.views.profile.show_by_slug", args=[p.slug]))

        self.assertEqual(p.text, params['text'])
        self.assertEqual(p.name, params['name'])

    @TestCaseEx.superuser
    def test_update_with_ajax_should_update_values(self):
        p = Profile.objects.create(name=u"some_new_name")

        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        response = self.can_post("profiles.views.profile.update", params=params, pargs=[p.pk], ajax=True)

        data = json.loads(response.content)
        p = Profile.objects.get(pk=p.pk)

        self.assertEqual(data['fields']['text'], params['text'])
        self.assertEqual(int(data['pk']), p.pk)
        self.assertEqual(p.text, params['text'])
        self.assertEqual(data['fields']['name'], params['name'])
        self.assertEqual(p.name, params['name'])

    def test_guest_cant_remove(self):
        p = Profile.objects.create(name=u"new item")
        self.redirect_on_post("profiles.views.profile.remove", pargs=[p.pk])
        self.redirect_on_get("profiles.views.profile.remove", pargs=[p.pk])

    @TestCaseEx.login
    def test_simple_user_cant_remove(self):
        p = Profile.objects.create(name=u"new item")
        self.redirect_on_post("profiles.views.profile.remove", pargs=[p.pk])
        self.redirect_on_get("profiles.views.profile.remove", pargs=[p.pk])

    @TestCaseEx.superuser
    def test_remove_should_remove_profile(self):
        p = Profile.objects.create(name=u"new item")
        self.assertEqual(1, Profile.objects.filter(pk=p.pk).count())

        response = self.redirect_on_get("profiles.views.profile.remove", pargs=[p.pk])
        self.assertRedirects(response, reverse("profiles.views.profile.index"))

        self.assertEqual(0, Profile.objects.filter(pk=p.pk).count())

    @TestCaseEx.superuser
    def test_remove_on_ajax_should_remove_profile(self):
        p = Profile.objects.create(name=u"new item")
        self.assertEqual(1, Profile.objects.filter(pk=p.pk).count())

        response = self.can_get("profiles.views.profile.remove", pargs=[p.pk], ajax=True)

        self.assertEqual(0, Profile.objects.filter(pk=p.pk).count())



