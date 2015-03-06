from app.utils import TestCaseEx
from profiles.models import Profile


class TestProfilesViews(TestCaseEx):
    def test_anyone_can_see_index_page(self):
        self.can_get("profiles.views.index")

    def test_anyone_can_check_profile(self):
        p = Profile.objects.create(name="somename")
        self.can_get("profiles.views.show", {
            "id": p.pk
        })

    @TestCaseEx.login
    def test_logged_user_can_see_more_data(self):
        pass

    def test_guest_cant_add(self):
        self.cant_post("profiles.views.add")
        self.cant_get("profiles.views.add")

    @TestCaseEx.login
    def test_adding_should_create_new_profile(self):
        self.can_get("profiles.views.add")  # check that we can get add page

        count_before = Profile.objects.count()
        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        self.can_post("profiles.views.add", params)
        self.assertEqual(count_before + 1, Profile.objects.count())

        # check for newely added profile
        new_profile = Profile.objects.order_by("-pk").first()
        self.assertEqual(new_profile.text, params['text'])
        self.assertEqual(new_profile.name, params['name'])

    def test_guest_cant_update(self):
        self.cant_post("profiles.views.update")
        self.cant_get("profiles.views.update")

    @TestCaseEx.login
    def test_update_should_update_values(self):
        p = Profile.objects.create(name="some_new_name")

        self.can_get("profiles.views.update", {
            "id": p.id
        })  # check that we can get update page

        params = {
            'text': '1928laksldjas',
            'name': 'alsjdlaskdjlsd'
        }
        self.can_post("profiles.views.update", params)
        p = Profile.objects.get(pk=p.pk)
        self.assertEqual(p.text, params['text'])
        self.assertEqual(p.name, params['name'])

    def test_guest_cant_remove(self):
        self.cant_post("profiles.views.remove")
        self.cant_get("profiles.views.remove")


    @TestCaseEx.login
    def test_remove_should_remove_profile(self):
        p = Profile.objects.create("new item")
        self.assertEqual(1, Profile.objects.filter(pk=p.pk))
        self.can_post("profiles.views.remove", {
            "id": p.pk
        })
        self.assertEqual(0, Profile.objects.filter(pk=p.pk))



