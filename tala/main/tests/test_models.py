from django.utils import unittest
from django.contrib.auth.models import User, Group
from tala.main.models import get_or_create_room, Message


class BasicRoomTest(unittest.TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="testgroup")
        self.room = get_or_create_room(group=self.group)

    def tearDown(self):
        self.room.delete()
        self.group.delete()

    def test_unicode(self):
        self.assertEquals(str(self.room), "testgroup")

    def test_get_absolute_url(self):
        self.assertEquals(
            self.room.get_absolute_url(),
            "/room/%d/" % self.room.id)

    def test_recent_messages(self):
        self.assertEquals(
            self.room.recent_messages(), [])


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="testgroup")
        self.room = get_or_create_room(group=self.group)
        self.user = User.objects.create(username="testuser")
        self.message = Message.objects.create(
            room=self.room,
            user=self.user,
            text="test message")

    def tearDown(self):
        self.message.delete()
        self.room.delete()
        self.group.delete()
        self.user.delete()

    def test_unicode(self):
        self.assertTrue('test message' in str(self.message))
        self.assertTrue('testuser' in str(self.message))

    def test_get_absolute_url(self):
        self.assertTrue('/archive/' in self.message.get_absolute_url())
        self.assertTrue('#message-' in self.message.get_absolute_url())
