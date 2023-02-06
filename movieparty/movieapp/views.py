from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import MovieForm, RoomForm
from .models import Movie, Room
from chatapp.models import ChatRoom


def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('rooms_list'))
    else:
        form = RoomForm()
    return render(request, 'movieapp/room_create.html', {'form': form})


def room_delete(request, item_id):
    item = Room.objects.get(pk=item_id)
    chat_item = ChatRoom.objects.get(name=item_id)
    chat_item.delete()
    item.delete()
    return HttpResponseRedirect(reverse_lazy('rooms_list'))


def room_update(request, item_id):
    instance = get_object_or_404(Room, id=item_id)
    form = RoomForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('rooms_list'))
    return render(request, 'movieapp/room_update.html', {'form': form})


def rooms_list(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'movieapp/rooms_list.html', context=context)


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('movies_list'))
    else:
        form = MovieForm()
    return render(request, 'movieapp/movie_create.html', {'form': form})


def movies_list(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/movies_list.html', context=context)


def movie_room(request, item_id):
    item = Room.objects.get(pk=item_id)
    movie = item.movie
    return render(request, 'movieapp/movie_room.html', {'item': item, 'video': movie.video})


@login_required
def base_views(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/base.html', context=context)
