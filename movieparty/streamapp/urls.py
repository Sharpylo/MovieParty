from django.urls import path

from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.watch_movie, name='watch_movie'),
]
