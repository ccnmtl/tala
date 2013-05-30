from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User, Group
from tala.main.models import get_or_create_room


class LoggedOutTest(unittest.TestCase):
    """ make sure that we don't have access to anything
    if we're not logged in """

    def setUp(self):
        self.c = Client()
        self.group = Group.objects.create(name="testgroup")
        self.room = get_or_create_room(group=self.group)

    def tearDown(self):
        self.room.delete()
        self.group.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)

    def test_room(self):
        response = self.c.get(self.room.get_absolute_url())
        self.assertEquals(response.status_code, 302)

    def test_fresh_token(self):
        response = self.c.get(self.room.get_absolute_url() + "fresh_token/")
        self.assertEquals(response.status_code, 302)

    def test_post(self):
        response = self.c.get(self.room.get_absolute_url() + "post/")
        self.assertEquals(response.status_code, 302)


class LoggedInTest(unittest.TestCase):
    """ Now that we're logged in, we should be able
    to access our room, get a token, etc."""

    def setUp(self):
        self.c = Client()
        self.group = Group.objects.create(name="testgroup")
        self.room = get_or_create_room(group=self.group)
        self.user = User.objects.create(username="testuser")
        self.user.set_password("test")
        self.user.groups.add(self.group)
        self.user.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.room.delete()
        self.group.delete()
        self.user.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_room(self):
        response = self.c.get(self.room.get_absolute_url())
        self.assertEquals(response.status_code, 200)

    def test_fresh_token(self):
        response = self.c.get(self.room.get_absolute_url() + "fresh_token/")
        self.assertEquals(response.status_code, 200)
