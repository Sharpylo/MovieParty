from django.urls import path

from . import views

urlpatterns = [
    path('check-password/<int:room_id>/', views.check_password, name='check_password'),
    path('chat-room/<int:room_name>/', views.chat_room_view, name='chat_room_view'),
]
