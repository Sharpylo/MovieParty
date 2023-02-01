from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import os

from .forms import MovieForm, RoomForm
from .models import Movie, Room


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
            response = {}
            for k in form.errors:
                response[k] = form.errors[k][0]
            return HttpResponse({"response": response})
    else:
        form = MovieForm()
    return render(request, 'movieapp/movie_create.html', {'form': form})


def movie_delete(request, item_id):
    item = Movie.objects.get(pk=item_id)
    if item.video:
        if os.path.exists(item.video.path):
            os.remove(item.video.path)
    if item.cover_image:
        if os.path.exists(item.cover_image.path):
            os.remove(item.cover_image.path)
    item.delete()
    return HttpResponseRedirect(reverse_lazy('movies_list'))


def movie_update(request, item_id):
    instance = get_object_or_404(Movie, id=item_id)
    if request.method == 'POST' or request.method == 'FILES':
        form = MovieForm(request.POST or request.FILES, instance=instance)
        if form.is_valid():
            if instance.video:
                if os.path.exists(instance.video.path):
                    os.remove(instance.video.path)
            if instance.cover_image:
                if os.path.exists(instance.cover_image.path):
                    os.remove(instance.cover_image.path)
            item = form.save(commit=False)
            item.save()
            return HttpResponseRedirect(reverse_lazy('movies_list'))
    else:
        form = MovieForm(instance=instance)
    return render(request, 'movieapp/movie_update.html', {'form': form})


def movies_list(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/movies_list.html', context=context)


def base_views(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/base.html', context=context)
