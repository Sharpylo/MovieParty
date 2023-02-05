from django.urls import path

from . import views

urlpatterns = [
    path('', views.chat_index_view, name='chat_index_view'),
    path('<str:room_name>/', views.chat_room_view, name='chat_room_view'),
]