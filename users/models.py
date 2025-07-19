from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="e-mail")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    country = CountryField(default='ru', blank=False, null=False, blank_label='Выберите страну')
    avatar = models.ImageField(upload_to='Users/avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return f'{self.username}  e-mail: {self.email}  country: {self.country}  phone: {self.phone_number}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
