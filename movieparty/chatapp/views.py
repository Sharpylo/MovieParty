from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponseForbidden

from movieapp.models import Room, Movie
from .models import ChatRoom


@login_required
def check_password(request, room_id):
    """
        Проверяет пароль для входа в комнату чата.

        Если пользователь авторизован и введенный пароль совпадает с паролем комнаты, то
        происходит перенаправление на страницу чата. В противном случае отображается сообщение
        об ошибке.
    """
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == room.password:
            return redirect('chat_room_view', room_name=room_id)
        else:
            messages.error(request, 'Неверный пароль')
    context = {'room': room}
    return render(request, 'chatapp/check_password.html', context)


def _handle_post_request(request, room, room_name):
    """
    Функция для обработки POST-запросов для chat_room_view
    """
    if request.method == 'POST':
        if request.user == room.created_by:
            movie_url = request.POST.get('movie_url')
            if movie_url:
                room.movie_url = movie_url
                room.save()
        else:
            return HttpResponseForbidden()


def chat_room_view(request, room_name):
    """
    Главная функция для отображения комнаты чата.
    """
    room = get_object_or_404(Room, pk=room_name)
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    movies = Movie.objects.all()

    _handle_post_request(request, room, room_name)
    is_owner = request.user == room.created_by

    return render(request, 'chatapp/chat_room.html', {
        'room': chat_room,
        'room_video': room,
        'room_name': room.name,
        'movies': movies,
        'movie_id': room_name,
        'selected_movie_url': room.movie_url,
        'is_owner': is_owner,
    })
