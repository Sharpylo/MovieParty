from django.urls import path
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.base_views, name='base_views'),
    path('movie-create/', views.movie_create, name='movie_create'),
    path('movies-list/', views.movies_list, name='movies_list'),
    path('movies-search/', views.movie_search, name='movie_search'),
    path('movies-filter/', views.movie_filter, name='movie_filter'),
    path('movies-card/<int:item_id>/', views.movies_card, name='movies_card'),

    path('room-create/', views.room_create, name='room_create'),
    path('rooms-list/', views.rooms_list, name='rooms_list'),
    path('room-delete/<int:item_id>/', views.room_delete, name='room_delete'),
    path('room-update/<int:item_id>/', views.room_update, name='room_update'),
]
