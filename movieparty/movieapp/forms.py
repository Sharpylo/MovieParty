from django import forms
from .models import Movie, Room
from datetime import datetime, timedelta


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'genre', 'cover_image', 'video']


class RoomForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}),
                                     label='Время начала фильма',
                                     required=False)
    duration_hours = forms.IntegerField(label='Продолжительность в часах', min_value=0, max_value=23)
    duration_minutes = forms.IntegerField(label='Продолжительность в минутах', min_value=0, max_value=59)
    end_time = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        duration_hours = cleaned_data.get("duration_hours")
        duration_minutes = cleaned_data.get("duration_minutes")
        if start_time and duration_hours is not None and duration_minutes is not None:
            end_time = start_time + timedelta(hours=duration_hours, minutes=duration_minutes)
            cleaned_data["end_time"] = end_time
        return cleaned_data

    class Meta:
        model = Room
        fields = ['name', 'movie', 'start_time', 'end_time', 'password']



