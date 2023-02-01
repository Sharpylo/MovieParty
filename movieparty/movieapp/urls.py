from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_views, name='base_views'),
    path('movie-create/', views.movie_create, name='movie_create'),
    path('movies-list/', views.movies_list, name='movies_list'),
    path('movie-delete/<int:item_id>/', views.movie_delete, name='movie_delete'),
    path('movie-update/<int:item_id>/', views.movie_update, name='movie_update'),
    path('room-create/', views.room_create, name='room_create'),
    path('rooms-list/', views.rooms_list, name='rooms_list'),
    path('room-delete/<int:item_id>/', views.room_delete, name='room_delete'),
    path('room-update/<int:item_id>/', views.room_update, name='room_update'),
]
