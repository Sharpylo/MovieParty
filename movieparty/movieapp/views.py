from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import MovieForm, RoomForm, RatingForm, ReviewForm
from .models import Movie, Room, Genre, Country, Rating, Review

from rest_framework import viewsets, status
from .serializers import MovieSerializer, CountrySerializer, GenreSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


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


def room_search(request):
    """
        Поиск комнат по названию.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка комнат со списком всех комнат, в названии которых содержится поисковый запрос.
    """
    query = request.GET.get('q')
    rooms = Room.objects.filter(name__icontains=query)
    return render(request, 'movieapp/rooms_list.html', {'rooms': rooms})


def room_filter(request):
    """
            Фильтр комнат по наличию пароля.

            Аргументы:
                request: объект HttpRequest, представляющий текущий запрос.

            Возвращает:
                Выводит страницу списка комнат со списком всех комнат с паролем или без

    """
    if request.method == "GET":
        has_password = request.GET.get("has_password")
        if has_password == 'yes':
            rooms = Room.objects.filter(has_password=True)
        elif has_password == 'no':
            rooms = Room.objects.filter(has_password=False)
        else:
            rooms = Room.objects.all()
        return render(request, "movieapp/rooms_list.html", {"rooms": rooms})


@login_required(login_url='/accounts/login')
def rooms_list(request):
    """
        Вывод списка всех комнат.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка комнат со списком всех комнат.
    """
    rooms_list = Room.objects.all().order_by('-created_at')
    # Обработка выбора количества элементов на странице
    items_per_page_r = request.GET.get('items_per_page_r')
    if items_per_page_r is None:
        items_per_page_r = 10
    else:
        items_per_page_r = int(items_per_page_r)
    paginator = Paginator(rooms_list, items_per_page_r)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)
    context = {'rooms': rooms, 'items_per_page_r': items_per_page_r}
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
    all_movies = Movie.objects.all()
    genre = Genre.objects.all()

    # Обработка выбора количества элементов на странице
    items_per_page = request.GET.get('items_per_page')
    if items_per_page is None:
        items_per_page = 12
    else:
        items_per_page = int(items_per_page)
    paginator = Paginator(all_movies, items_per_page)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    context = {'movies': movies, 'genres': genre, 'items_per_page': items_per_page}
    return render(request, 'movieapp/movies_list.html', context=context)


def _get_movie_ratings(movie):
    '''
    Функция по подсчету среднего рейтинга
    '''
    ratings = movie.movie_ratings.all()
    avg_rating = 0
    num_ratings = len(ratings)
    if num_ratings > 0:
        total_rating = sum([rating.value for rating in ratings])
        avg_rating = round(total_rating / num_ratings, 1)
    return ratings, avg_rating, num_ratings


def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies_card', item_id=movie.id)
    context = {
        'movie': movie,
        'form': form
    }
    return render(request, 'movieapp/movies_card.html', context)


@login_required
def movies_card(request, item_id):
    """
        Отображает подробное представление фильма, включая информацию о фильме,
        трейлере, среднем рейтинге и рейтинге пользователя (если он аутентифицирован).
        Если пользователь отправляет оценку через POST-запрос, сохраняет или обновляет оценку
        для текущего пользователя и фильма, а также выводит сообщение об успехе или ошибке
        соответственно.

        Аргументы:
        - request: объект HttpRequest, представляющий текущий запрос
        - item_id: целое число, представляющее идентификатор объекта Movie, который должен быть отображен.

        Возвращает:
        - HttpResponse объект, отображающий шаблон 'movieapp/movies_card.html'
          со следующими контекстными переменными:
            - 'movie': объект Movie с указанным ID
            - 'trailer': строка, представляющая URL-адрес трейлера фильма на YouTube
            - 'rating': объект Rating, соответствующий текущему пользователю и фильму,
              или None, если пользователь не аутентифицирован или еще не оценил фильм.
            - 'rating_form': Объект RatingForm для отображения и проверки пользовательского
              рейтинга через POST-запрос
            - 'avg_rating': плавающая величина, представляющая средний рейтинг для фильма
            - 'num_ratings': целое число, представляющее общее количество оценок для фильма
    """
    movie = get_object_or_404(Movie, pk=item_id)
    rating_form = RatingForm(request.POST or None)
    ratings, avg_rating, num_ratings = _get_movie_ratings(movie)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.user.ratings.filter(movie=movie).first()
        rating_form = RatingForm(request.POST, instance=rating)
        if rating_form.is_valid():
            rating_obj = rating_form.save(commit=False)
            rating_obj.user = request.user
            rating_obj.movie = movie
            rating_obj.save()
            if rating:
                messages.success(request, 'Ваш рейтинг успешно обновлен!')
            else:
                messages.success(request, 'Ваш рейтинг успешно сохранен!')
        else:
            messages.error(request, 'Некорректное значение рейтинга')
    else:
        rating = request.user.ratings.filter(movie=movie).first() if request.user.is_authenticated else None
        rating_form = RatingForm(instance=rating)

    link_trailer = 'https://www.youtube.com/embed/' + movie.trailer.split('/')[-1]
    context = {
        'movie': movie,
        'trailer': link_trailer,
        'rating': rating,
        'rating_form': rating_form,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
        'form': ReviewForm(),
        'reviews': reviews,
    }
    return render(request, 'movieapp/movies_card.html', context)


def movies_rating_list(request):
    """
        Функция просмотра для отображения списка фильмов, отсортированных по среднему рейтингу или количеству оценок.

        Аргументы:
        - request: объект HttpRequest

        Возвращает:
        - HttpResponse объект, содержащий отрисованный шаблон movieapp/movies_rating_list.html

        Функция извлекает список всех фильмов из модели Movie, а затем вычисляет средний рейтинг и количество
        оценок для каждого фильма с помощью вспомогательной функции _get_movie_ratings. Затем данные о фильмах сортируются в зависимости от
        значения параметра запроса sort_by, который по умолчанию имеет значение 'avg_rating'. Параметр запроса sort_order используется для того, чтобы
        определяет, в каком порядке сортировать - по возрастанию или по убыванию, и по умолчанию имеет значение 'desc'.

        Функция рендерит шаблон movieapp/movies_rating_list.html, передавая отсортированные данные фильмов, текущее значение sort_order и текущее значение sort_by.
        sort_by и текущее значение sort_order в контекстном словаре. Шаблон отображает данные о фильмах в
        в виде таблицы, каждая строка которой представляет фильм, его название, средний рейтинг и количество оценок.
     """
    sort_by = request.GET.get('sort_by', 'avg_rating')
    sort_order = request.GET.get('sort_order', 'desc')
    movies = Movie.objects.all()
    movie_data = []
    for movie in movies:
        ratings, avg_rating, num_ratings = _get_movie_ratings(movie)
        movie_data.append({'title': movie.title, 'avg_rating': avg_rating, 'num_ratings': num_ratings, 'id': movie.id})
    if sort_by == 'num_ratings':
        movie_data.sort(key=lambda x: x['num_ratings'], reverse=sort_order == 'desc')
    else:
        movie_data.sort(key=lambda x: x['avg_rating'], reverse=sort_order == 'desc')
    context = {'movie_data': movie_data, 'sort_by': sort_by,
               'sort_order': sort_order}
    return render(request, 'movieapp/movies_rating_list.html', context)


def movie_search(request):
    """
        Поиск фильмов по названию.

        Аргументы:
            request: объект HttpRequest, представляющий текущий запрос.

        Возвращает:
            Выводит страницу списка фильмов со списком всех фильмов, в названии которых содержится поисковый запрос.
    """
    query = request.GET.get('q')
    movies = Movie.objects.filter(Q(title__icontains=query) | Q(title_eng__icontains=query))
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
    movies_top = []
    for movie in movies:
        ratings, avg_rating, num_ratings = _get_movie_ratings(movie)
        movies_top.append({'title': movie.title, 'avg_rating': avg_rating, 'num_ratings': num_ratings,
                           'cover_image': movie.cover_image, 'description': movie.description, 'id': movie.id})
    movies_top = sorted(movies_top, key=lambda x: x['avg_rating'], reverse=True)

    context = {'movies': movies, 'movies_top': movies_top[:5]}
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
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the list of rating IDs from the request data
        ratings = request.data.get('ratings', [])

        # Create a new movie instance
        self.perform_create(serializer)

        # Set the ratings for the movie using the set() method
        movie = serializer.instance
        movie.ratings.set(ratings)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoomViewSet(viewsets.ModelViewSet):
    """
        Набор представлений для просмотра и редактирования экземпляров комнат.
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
