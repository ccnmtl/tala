from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from simplejson import dumps
from tala.main.models import User, Room, Message, get_or_create_room
import zmq

zmq_context = zmq.Context()
BROKER_URL = "tcp://localhost:5555"
ZMQ_APPNAME = "tala"

@login_required
@render_to('main/index.html')
def index(request):
    rooms = [get_or_create_room(g) for g in request.user.groups.all()]
    return dict(rooms=rooms)


@login_required
@render_to('main/room.html')
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return dict(room=room)


@login_required
def post_to_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    text = request.POST.get('text', '')
    if text:
        m = Message.objects.create(room=room, user=request.user, text=text)
        # publish it via the zmq broker
        socket = zmq_context.socket(zmq.REQ)
        socket.connect(BROKER_URL)
        # the message we are broadcasting
        md = dict(room_id=room.id,
                  username=m.user.username,
                  message_text=m.text)
        # an envelope that contains that message serialized
        # and the address that we are publishing to
        e = dict(address="%s.message.room_%d" % (ZMQ_APPNAME, room.id),
                 content=dumps(md))
        # send it off to the broker
        socket.send(dumps(e))
        # wait for a response from the broker to be sure it was sent
        socket.recv()

    return HttpResponseRedirect(room.get_absolute_url())
