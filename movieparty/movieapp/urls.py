from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_views, name='base_views'),
    path('movie-create/', views.movie_create, name='movie_create'),
    path('movies-list/', views.movies_list, name='movies_list'),
    path('room-create/', views.room_create, name='room_create'),
]
