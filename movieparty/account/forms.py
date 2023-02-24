from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
        }


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'phone_number']
        labels = {
            'phone_number': 'Номер телефона',
        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
