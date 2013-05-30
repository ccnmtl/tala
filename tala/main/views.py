from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from datetime import datetime
import time
from random import randint
import hmac
import hashlib
from django.utils import simplejson
from tala.main.models import Room, Message, get_or_create_room
import zmq

zmq_context = zmq.Context()


def gen_token(request, room_id):
    username = request.user.username
    sub_prefix = "%s.room_%d" % (settings.ZMQ_APPNAME, room_id)
    pub_prefix = sub_prefix + "." + username
    now = int(time.mktime(datetime.now().timetuple()))
    salt = randint(0, 2**20)
    ip_address = (request.META.get("HTTP_X_FORWARDED_FOR", "")
                  or request.META.get("REMOTE_ADDR", ""))

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
@render_to('main/index.html')
def index(request):
    rooms = [get_or_create_room(g) for g in request.user.groups.all()]
    return dict(rooms=rooms)


@login_required
@render_to('main/room.html')
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return dict(room=room, token=gen_token(request, room.id),
                websockets_base=settings.WINDSOCK_WEBSOCKETS_BASE)


@login_required
def fresh_token(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return HttpResponse(
        simplejson.dumps(dict(token=gen_token(request, room.id))),
        mimetype="application/json")


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
                 content=simplejson.dumps(md))
        # send it off to the broker
        socket.send(simplejson.dumps(e))
        # wait for a response from the broker to be sure it was sent
        socket.recv()

    return HttpResponseRedirect(room.get_absolute_url())
