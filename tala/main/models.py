from django.db import models
from django.contrib.auth.models import User, Group


def get_or_create_room(group):
    r = Room.objects.filter(group=group)
    if r.count() > 0:
        return r[0]
    else:
        return Room.objects.create(group=group, title=group.name)


class Room(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField(max_length=256, default=u"unknown room")
    description = models.TextField(default=u"", blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/room/%d/" % self.id

    def recent_messages(self):
        """ just the most recent messages, chronological order """
        messages = list(self.message_set.all().order_by("-added")[:10])
        messages.reverse()
        return messages

    def unique_dates(self):
        """ list of dates that this room has messages from """
        return self.message_set.dates('added', 'day')


class Message(models.Model):
    room = models.ForeignKey(Room)
    user = models.ForeignKey(User)
    text = models.TextField(default=u"", blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added', ]

    def __unicode__(self):
        return "[%s] %s: %s" % (self.added, self.user.username, self.text)

    def get_absolute_url(self):
        return (
            self.room.get_absolute_url()
            + "archive/%04d-%02d-%02d/#message-%d" % (
                self.added.year,
                self.added.month,
                self.added.day,
                self.id))
