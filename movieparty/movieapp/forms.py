from django import forms
from .models import Movie, Room, Rating


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'genre', 'cover_image', 'video']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'has_password', 'password']
        widgets = {
            'has_password': forms.CheckboxInput(attrs={'id': 'has_password'}),
        }


class RatingForm(forms.ModelForm):
    value = forms.IntegerField(widget=forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]))

    class Meta:
        model = Rating
        fields = ('value',)
