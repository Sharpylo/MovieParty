from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование фильма')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    year = models.IntegerField(verbose_name='Год выпуска', null=True, blank=True)
    genre = models.CharField(max_length=50, verbose_name='Жанр', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', verbose_name='Изображение обложки', null=True, blank=True)
    video = models.FileField(upload_to='videos/', verbose_name='Ссылка на фильм', null=True, blank=True)


class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя комнаты')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Название фильма')
    password = models.CharField(max_length=50, verbose_name='Пароль для комнаты', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')


class Playlist(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Comment(models.Model):
    user = models.ForeignKey('userapp.User', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
