from django.shortcuts import get_object_or_404, render
from movieapp.models import Room, Movie
from .models import ChatRoom


def chat_room_view(request, room_name):
    room = get_object_or_404(Room, pk=room_name)
    movies = Movie.objects.all()
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)

    if request.method == 'POST':
        movie_url = request.POST.get('movie_url')
        if movie_url:
            # сохраняем выбранный фильм в базе данных
            room.movie_url = movie_url
            room.save()

    # передаем данные о фильме на страницу
    return render(request, 'chatapp/chat_room.html', {
        'room': chat_room,
        'room_video': room,
        'room_name': room.name,
        'movies': movies,
        'movie_id': room_name,
        'selected_movie_url': room.movie_url,
    })
