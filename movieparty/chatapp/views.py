from django.shortcuts import render

from .models import ChatRoom


def chat_index_view(request):
    return render(request, 'chatapp/chat_index.html', {
        'rooms': ChatRoom.objects.all(),
    })


def chat_room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chatapp/chat_room.html', {
        'room': chat_room,
    })
