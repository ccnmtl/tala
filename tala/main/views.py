from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from tala.main.models import User, Room, Message, get_or_create_room


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
    return HttpResponseRedirect(room.get_absolute_url())
