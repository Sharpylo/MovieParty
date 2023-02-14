from django.db import models
from django.utils.html import format_html


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название страны')

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование фильма')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    year = models.IntegerField(verbose_name='Год выпуска', null=True, blank=True)
    country = models.ManyToManyField(Country, verbose_name='Страны', related_name='movies')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры', related_name='movies')
    cover_image = models.ImageField(upload_to='covers/', verbose_name='Изображение обложки', null=True, blank=True)
    video = models.FileField(upload_to='videos/', verbose_name='Файл фильма', null=True, blank=True)
    trailer = models.TextField(verbose_name='Трейлер', null=True, blank=True)
    link_movie = models.TextField(verbose_name='Ссылка на фильм', null=True, blank=True)

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


class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя комнаты')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Название фильма')
    password = models.CharField(max_length=50, verbose_name='Пароль для комнаты', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='Время начала фильма')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Время конца фильма')

    def __str__(self):
        return self.name
