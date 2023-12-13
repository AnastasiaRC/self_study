from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    AUTHOR = 'author', _('Author')
    MODERATOR = 'moderator', _('Moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    last_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    first_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)
    image = models.ImageField(upload_to='media/users/', verbose_name='Картинка', **NULLABLE)
    role = models.CharField(max_length=20, choices=UserRoles.choices, verbose_name='Роль', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Авторизация')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('id',)
