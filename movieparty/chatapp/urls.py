from django.urls import path

from . import views

urlpatterns = [
    path('chat-room/<str:room_name>/', views.chat_room_view, name='chat_room_view'),
]
