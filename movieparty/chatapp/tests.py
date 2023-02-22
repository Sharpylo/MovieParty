from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from movieapp.models import Room, Movie
from chatapp.models import ChatRoom
from django.core.files.uploadedfile import SimpleUploadedFile


class CheckPasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.room = Room.objects.create(name='Test Room', password='testpassword123')

    def test_check_password_with_correct_password(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('check_password', args=[self.room.id]), {'password': 'testpassword123'})
        self.assertRedirects(response, reverse('chat_room_view', args=[self.room.id]))

    def test_check_password_with_incorrect_password(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('check_password', args=[self.room.id]), {'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный пароль')
