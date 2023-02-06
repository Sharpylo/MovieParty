from django.shortcuts import render

from movieapp.models import Room
from .models import ChatRoom


def chat_room_view(request, room_name):
    item = Room.objects.get(pk=int(room_name))
    movie = item.movie
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chatapp/chat_room.html', {
        'room': chat_room, 'room_name': item.name, 'video1': movie.video,
    })
