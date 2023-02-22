from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponseForbidden

from movieapp.models import Room, Movie
from .models import ChatRoom


@login_required
def check_password(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == room.password:
            return redirect('chat_room_view', room_name=room_id)
        else:
            messages.error(request, 'Неверный пароль')
    context = {'room': room}
    return render(request, 'chatapp/check_password.html', context)


def chat_room_view(request, room_name):
    room = get_object_or_404(Room, pk=room_name)
    movies = Movie.objects.all()
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)

    if request.method == 'POST':
        if request.user == room.created_by:
            movie_url = request.POST.get('movie_url')
            if movie_url:
                # сохраняем выбранный фильм в базе данных
                room.movie_url = movie_url
                room.save()
        else:
            return HttpResponseForbidden()

    if request.user == room.created_by:
        is_owner = True
    else:
        is_owner = False

    # передаем данные о фильме на страницу
    return render(request, 'chatapp/chat_room.html', {
        'room': chat_room,
        'room_video': room,
        'room_name': room.name,
        'movies': movies,
        'movie_id': room_name,
        'selected_movie_url': room.movie_url,
        'is_owner': is_owner,
    })
