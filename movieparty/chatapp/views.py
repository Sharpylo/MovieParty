from django.shortcuts import render
from movieapp.models import Room
from .models import Message


def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room)
    return render(request, 'chatapp/chat.html', {'room': room, 'messages': messages})
