from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import MovieForm, RoomForm
from .models import Movie, Room, Genre, Country
from chatapp.models import ChatRoom

from rest_framework import viewsets
from .serializers import MovieSerializer, CountrySerializer, GenreSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@login_required(login_url='/accounts/login')
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rooms_list'))  # исправлено: reverse_lazy -> reverse
    else:
        form = RoomForm()
    return render(request, 'movieapp/room_create.html', {'form': form})


@login_required(login_url='/accounts/login')
def room_delete(request, item_id):
    try:
        item = Room.objects.get(pk=item_id)
        chat_item, created = ChatRoom.objects.get_or_create(name=str(item_id))
        chat_item.delete()
        item.delete()
        return HttpResponseRedirect(reverse_lazy('rooms_list'))
    except Room.DoesNotExist:
        # обработать случай, когда комната не существует
        return HttpResponse('Room does not exist', status=404)


@login_required(login_url='/accounts/login')
def room_update(request, item_id):
    instance = get_object_or_404(Room, id=item_id)
    form = RoomForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('rooms_list'))
    return render(request, 'movieapp/room_update.html', {'form': form})


@login_required(login_url='/accounts/login')
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
    genre = Genre.objects.all()
    context = {'movies': movies, 'genres': genre}
    return render(request, 'movieapp/movies_list.html', context=context)


def movies_card(request, item_id):
    movie = Movie.objects.get(pk=item_id)
    link_trailer = 'https://www.youtube.com/embed/' + movie.trailer.split('/')[-1]
    return render(request, 'movieapp/movies_card.html', {'movie': movie, 'trailer': link_trailer})


def movie_search(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'movieapp/movies_list.html', {'movies': movies})


def movie_filter(request):
    if request.method == "GET":
        genre_name = request.GET.get("genre")
        if genre_name:
            movies = Movie.objects.filter(genre__name=genre_name)
        else:
            movies = Movie.objects.all()
        return render(request, "movieapp/movies_list.html", {"movies": movies, "selected_genre": genre_name})


@login_required(login_url='/accounts/login')
def base_views(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/base.html', context=context)


# Serializers

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
