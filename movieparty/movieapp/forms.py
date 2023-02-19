from django import forms
from .models import Movie, Room
from datetime import datetime, timedelta


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'genre', 'cover_image', 'video']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'password']
