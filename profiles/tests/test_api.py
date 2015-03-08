from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCase


class TestProfilePasskeysResource(ResourceTestCase):
    def setUp(self):
        self.root = User.objects.create_superuser('root', 'mailm@mail.ru', "12345")
        self.user = User.objects.create_user('default', 'admin@admin.ru', "12345")
        super(TestProfilePasskeysResource, self).setUp()

    def test_guest_cant_get_access_profile_passkeys_resource(self):
        url = "/api/v1/profilepasskeys/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_simple_user_cant_access_profile_passkeys_resource(self):
        self.client.login(username=self.user.username, password="12345")
        url = "/api/v1/profilepasskeys/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_superuser_can_access_profile_passkeys_resources(self):
        self.client.login(username=self.root.username, password="12345")
        url = "/api/v1/profilepasskeys/?format=json"
        resp = self.client.get(url)
        self.assertHttpOK(resp)


class TestProfileResource(ResourceTestCase):
    def setUp(self):
        self.root = User.objects.create_superuser('root', 'mailm@mail.ru', "12345")
        self.user = User.objects.create_user('default', 'admin@admin.ru', "12345")
        super(TestProfileResource, self).setUp()

    def test_guest_cant_get_access_profile_resource(self):
        url = "/api/v1/profile/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_simple_user_cant_access_profile_resource(self):
        self.client.login(username=self.user.username, password="12345")
        url = "/api/v1/profile/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_superuser_can_access_profile_passkeys_resources(self):
        self.client.login(username=self.root.username, password="12345")
        url = "/api/v1/profile/?format=json"
        resp = self.client.get(url)
        self.assertHttpOK(resp)


class TestUserResource(ResourceTestCase):
    def setUp(self):
        self.root = User.objects.create_superuser('root', 'mailm@mail.ru', "12345")
        self.user = User.objects.create_user('default', 'admin@admin.ru', "12345")
        super(TestUserResource, self).setUp()

    def test_guest_cant_get_access_profile_resource(self):
        url = "/api/v1/user/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_simple_user_cant_access_profile_resource(self):
        self.client.login(username=self.user.username, password="12345")
        url = "/api/v1/user/?format=json"
        resp = self.client.get(url)
        self.assertHttpUnauthorized(resp)

    def test_superuser_can_access_profile_passkeys_resources(self):
        self.client.login(username=self.root.username, password="12345")
        url = "/api/v1/user/?format=json"
        resp = self.client.get(url)
        self.assertHttpOK(resp)
