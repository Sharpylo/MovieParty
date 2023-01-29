from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    year = models.IntegerField()
    genre = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='covers')
    video = models.FileField(upload_to='videos')


class Room(models.Model):
    name = models.CharField(max_length=50)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
