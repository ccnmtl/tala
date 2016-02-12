from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from datetime import datetime
import time
from random import randint
import hmac
import hashlib
import json
from tala.main.models import Room, Message, get_or_create_room
import zmq

zmq_context = zmq.Context()


def gen_token(request, room_id):
    username = request.user.username
    sub_prefix = "%s.room_%d" % (settings.ZMQ_APPNAME, room_id)
    pub_prefix = sub_prefix + "." + username
    now = int(time.mktime(datetime.now().timetuple()))
    salt = randint(0, 2 ** 20)
    ip_address = (request.META.get("HTTP_X_FORWARDED_FOR", "") or
                  request.META.get("REMOTE_ADDR", ""))

    hmc = hmac.new(settings.WINDSOCK_SECRET,
                   '%s:%s:%s:%d:%d:%s' % (username, sub_prefix,
                                          pub_prefix, now, salt,
                                          ip_address),
                   hashlib.sha1
                   ).hexdigest()
    return '%s:%s:%s:%d:%d:%s:%s' % (username, sub_prefix,
                                     pub_prefix, now, salt,
                                     ip_address, hmc)


@login_required
def index(request):
    rooms = [get_or_create_room(g) for g in request.user.groups.all()]
    return render(request, 'main/index.html', dict(rooms=rooms))


@login_required
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'main/room.html',
                  dict(room=room, token=gen_token(request, room.id),
                       websockets_base=settings.WINDSOCK_WEBSOCKETS_BASE))


@login_required
def room_archive(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'main/room_archive.html', dict(room=room))


@login_required
def room_archive_date(request, room_id, date):
    room = get_object_or_404(Room, pk=room_id)
    (year, month, day) = date.split('-')
    # TODO: deal with invalid dates (Feb 30th, etc)
    d = datetime(year=int(year), month=int(month), day=int(day))
    messages = room.message_set.filter(
        added__year=year,
        added__month=month,
        added__day=day)
    return render(request, 'main/room_archive_date.html',
                  dict(room=room, messages=messages, date=d))


@login_required
def fresh_token(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return HttpResponse(
        json.dumps(dict(token=gen_token(request, room.id))),
        content_type="application/json")


@login_required
def post_to_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    text = request.POST.get('text', '')
    if text:
        m = Message.objects.create(room=room, user=request.user, text=text)
        # publish it via the zmq broker
        socket = zmq_context.socket(zmq.REQ)
        socket.connect(settings.WINDSOCK_BROKER_URL)
        # the message we are broadcasting
        md = dict(room_id=room.id,
                  username=m.user.username,
                  message_text=m.text)
        # an envelope that contains that message serialized
        # and the address that we are publishing to
        e = dict(address="%s.room_%d" % (settings.ZMQ_APPNAME, room.id),
                 content=json.dumps(md))
        # send it off to the broker
        socket.send(json.dumps(e))
        # wait for a response from the broker to be sure it was sent
        socket.recv()

    return HttpResponseRedirect(room.get_absolute_url())
