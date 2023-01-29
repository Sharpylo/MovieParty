from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import MovieForm, RoomForm
from .models import Movie


def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rooms_list')
    else:
        form = RoomForm()
        return render(request, 'movieapp/room_create.html', {'form': form})


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies_list')
    else:
        form = MovieForm()
    return render(request, 'movieapp/movie_create.html', {'form': form})


def movies_list(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/movies_list.html', context=context)


def base_views(request):
    return render(request, 'movieapp/base.html')
