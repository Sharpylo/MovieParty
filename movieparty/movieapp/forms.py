from django import forms
from .models import Movie, Room, Playlist, Comment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'genre', 'cover_image', 'video']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'movie', 'password']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['room', 'movie', 'start_time', 'end_time']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'room', 'content']
