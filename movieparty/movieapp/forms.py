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
    value = forms.ChoiceField(choices=[(str(i), i) for i in range(1, 6)], widget=forms.RadioSelect)

    class Meta:
        model = Rating
        fields = ('value',)
