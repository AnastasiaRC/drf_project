from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('Member')
    MODERATOR = 'moderator', _('Moderator')


class User(AbstractUser):
    username = None
    avatar = models.ImageField(upload_to='media/users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон',**NULLABLE)
    city = models.CharField(max_length=30, verbose_name='город', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    # is_manager = models.BooleanField(default=False, verbose_name='менеджер')
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='Role', )
    is_active = models.BooleanField(default=True, verbose_name='aктивность пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
