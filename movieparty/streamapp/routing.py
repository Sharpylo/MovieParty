from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/movie/<int:pk>/', consumers.MovieConsumer.as_asgi()),
]
