from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Ник')
    image = models.ImageField(verbose_name='Аватарка', default='account/account.jpg', upload_to='account/profile_pics')
    bio = models.TextField(verbose_name='О себе', max_length=500, null=True, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
