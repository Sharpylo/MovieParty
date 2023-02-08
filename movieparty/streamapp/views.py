from django.shortcuts import render
from movieapp.models import Room


def watch_movie(request, movie_id):
    item = Room.objects.get(id=movie_id)
    movie = item.movie
    return render(request, 'streamapp/movie.html', {'movie': movie.video, 'movie_id': movie_id})
