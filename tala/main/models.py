from django.db import models
from django.contrib.auth.models import User, Group

class Room(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField(max_length=256, default=u"unknown room")
    description = models.TextField(default=u"", blank=True)

class Message(models.Model):
    room = models.ForeignKey(Room)
    user = models.ForeignKey(User)
    text = models.TextField(default=u"", blank=True)
    added = models.DateTimeField(auto_now_add=True)
