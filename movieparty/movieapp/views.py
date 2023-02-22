from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
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
    """
        Создать новую комнату.

        Args:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Если метод запроса GET, отображает форму создания комнаты.
            Если метод запроса POST и форма действительна, создает новую комнату с данными формы и
            перенаправляет к списку комнат.
    """
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            return HttpResponseRedirect(reverse('rooms_list'))
    else:
        form = RoomForm()
    return render(request, 'movieapp/room_create.html', {'form': form})


@login_required(login_url='/accounts/login')
def room_delete(request, item_id):
    """
        Удалить существующую комнату.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.
            item_id: ID удаляемой комнаты.

        Возвращает:
            Если комната существует и у текущего пользователя есть разрешение на ее удаление, удаляет комнату и перенаправляет
            к списку комнат. В противном случае возвращается HttpResponseForbidden или HttpResponse с сообщением об ошибке.
    """
    try:
        room = Room.objects.get(pk=item_id)
        if not room.can_edit(request.user):
            return HttpResponseForbidden('Вы не уполномочены выполнять это действие')
        room.delete()
        return HttpResponseRedirect(reverse('rooms_list'))
    except Room.DoesNotExist:
        return HttpResponse('Комната не существует', status=404)


@login_required(login_url='/accounts/login')
def room_update(request, item_id):
    """
        Обновление существующей комнаты.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.
            item_id: ID обновляемой комнаты.

        Возвращает:
            Если комната существует и текущий пользователь имеет право редактировать ее, отображает форму обновления комнаты с
            данными текущей комнаты. Если форма действительна, обновляет комнату и перенаправляет к списку комнат.
            В противном случае возвращается HttpResponseForbidden или HttpResponse с сообщением об ошибке.
    """
    room = get_object_or_404(Room, id=item_id)
    if not room.can_edit(request.user):
        return HttpResponseForbidden('Вы не авторизованы для выполнения этого действия')
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('rooms_list'))
    return render(request, 'movieapp/room_update.html', {'form': form})


@login_required(login_url='/accounts/login')
def rooms_list(request):
    """
        Вывод списка всех комнат.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка комнат со списком всех комнат.
    """
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'movieapp/rooms_list.html', context=context)


def movie_create(request):
    """
        Создать новый фильм.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Если метод запроса - GET, отображает форму создания фильма. Если форма действительна, создается новый
            фильм с данными формы и перенаправляет к списку фильмов.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('movies_list'))
    else:
        form = MovieForm()
    return render(request, 'movieapp/movie_create.html', {'form': form})


def movies_list(request):
    """
        Вывод списка всех фильмов.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка фильмов со списком всех фильмов и жанров.
    """
    movies = Movie.objects.all()
    genre = Genre.objects.all()
    context = {'movies': movies, 'genres': genre}
    return render(request, 'movieapp/movies_list.html', context=context)


def movies_card(request, item_id):
    """
    Вывод страницы с подробной информацией о конкретном фильме.

    Args:
        request: объект HttpRequest, представляющий текущий запрос.
        item_id: ID фильма, который необходимо отобразить.

    Возвращает:
        Выводит страницу с подробной информацией о выбранном фильме и его трейлере.

    link_trailer - переделывает ссылку для отображения трейлера на странице фильма
    """
    movie = Movie.objects.get(pk=item_id)
    link_trailer = 'https://www.youtube.com/embed/' + movie.trailer.split('/')[-1]
    return render(request, 'movieapp/movies_card.html', {'movie': movie, 'trailer': link_trailer})


def movie_search(request):
    """
        Поиск фильмов по названию.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка фильмов со списком всех фильмов, в названии которых содержится поисковый запрос.
    """
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'movieapp/movies_list.html', {'movies': movies})


def movie_filter(request):
    """
            Фильтр фильмов по жанру.

            Аргументы:
                request: объект HttpRequest, представляющий текущий запрос.

            Возвращает:
                Выводит страницу списка фильмов со списком всех фильмов, относящихся к выбранному жанру, или все фильмы.
                если жанр не выбран.
        """
    if request.method == "GET":
        genre_name = request.GET.get("genre")
        if genre_name:
            movies = Movie.objects.filter(genre__name=genre_name)
        else:
            movies = Movie.objects.all()
        return render(request, "movieapp/movies_list.html", {"movies": movies, "selected_genre": genre_name})


@login_required(login_url='/accounts/login')
def base_views(request):
    '''
    Основная функция.

        Эта функция представления отображает шаблон 'base.html' и передает словарь всех фильмов в контекст.
        Только аутентифицированные пользователи могут получить доступ к этому представлению.

    Аргументы:
        request: объект HttpRequest, представляющий текущий запрос.

    Возвращает:
        Отрисованный объект HttpResponse, содержащий шаблон 'base.html' и словарь всех фильмов.
    '''
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movieapp/base.html', context=context)


# Serializers

class CountryViewSet(viewsets.ModelViewSet):
    """
        Набор представлений для просмотра и редактирования экземпляров Country.
    """
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """
        Набор представлений для просмотра и редактирования экземпляров жанра.
    """
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class MovieViewSet(viewsets.ModelViewSet):
    """
        Набор представлений для просмотра и редактирования экземпляров Movie.
    """
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoomViewSet(viewsets.ModelViewSet):
    """
        Набор представлений для просмотра и редактирования экземпляров комнат.
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
