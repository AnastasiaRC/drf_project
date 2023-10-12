from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    avatar = models.ImageField(upload_to='media/users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон',**NULLABLE)
    city = models.CharField(max_length=30, verbose_name='город', **NULLABLE)
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    is_manager = models.BooleanField(default=False, verbose_name='менеджер')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
