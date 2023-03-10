from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.html import format_html
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название страны')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование фильма')
    title_eng = models.CharField(max_length=50, verbose_name='Наименование фильма на английском', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    year = models.IntegerField(verbose_name='Год выпуска', null=True, blank=True)
    country = models.ManyToManyField(Country, verbose_name='Страны', related_name='movies')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры', related_name='movies')
    cover_image = models.ImageField(upload_to='covers/', verbose_name='Изображение обложки', null=True, blank=True)
    roundabout_image = models.ImageField(upload_to='covers/', verbose_name='Изображение для карусели', null=True,
                                         blank=True)
    video = models.FileField(upload_to='videos/', verbose_name='Файл фильма', null=True, blank=True)
    trailer = models.TextField(verbose_name='Трейлер', null=True, blank=True)
    link_movie = models.TextField(verbose_name='Ссылка на фильм', null=True, blank=True)
    ratings = models.ManyToManyField(User, through='Rating', related_name='movie_ratings')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def get_image_html(self):
        if self.cover_image:
            return format_html('<img src="{}" width="100px" />'.format(self.cover_image.url))
        else:
            return "-"

    get_image_html.short_description = 'Изображение обложки'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)

    class Meta:
        unique_together = ('movie', 'user')
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.movie.title} - {self.user.username} - {self.value}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя комнаты')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Название фильма', null=True, blank=True)
    movie_url = models.CharField(max_length=50, verbose_name='URL фильма', null=True, blank=True)
    has_password = models.BooleanField(default=False, verbose_name='Требуется пароль')
    password = models.CharField(max_length=128, blank=True, verbose_name='Пароль для комнаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='Время начала фильма')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Время конца фильма')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.has_password = True
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def can_edit(self, user):
        return user == self.created_by

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
