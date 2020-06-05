import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from testapps.models import App
from testapps.serializers import AppSerializer


class AppListCreateAPIViewTestCase(APITestCase):
    url = reverse("testapps:list")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_app(self):
        response = self.client.post(self.url, {"name": "Clean the room!"})
        self.assertEqual(201, response.status_code)

    def test_user_testapps(self):
        """
        Test to verify user testapps list
        """
        App.objects.create(user=self.user, name="Clean the car!")
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == App.objects.count())


class AppDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.app = App.objects.create(user=self.user, name="Call Mom!")
        self.url = reverse("testapps:detail", kwargs={"pk": self.app.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_app_object_bundle(self):
        """
        Test to verify app object bundle
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        app_serializer_data = AppSerializer(instance=self.app).data
        response_data = json.loads(response.content)
        self.assertEqual(app_serializer_data, response_data)

    def test_app_object_update_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        response = self.client.put(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

        # HTTP PATCH
        response = self.client.patch(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

    def test_app_object_update(self):
        response = self.client.put(self.url, {"name": "Call Dad!"})
        response_data = json.loads(response.content)
        app = App.objects.get(id=self.app.id)
        self.assertEqual(response_data.get("name"), app.name)

    def test_app_object_partial_update(self):
        response = self.client.patch(self.url, {"done": True})
        response_data = json.loads(response.content)
        app = App.objects.get(id=self.app.id)
        self.assertEqual(response_data.get("done"), app.done)

    def test_app_object_delete_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_app_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
