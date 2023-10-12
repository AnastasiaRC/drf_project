from django.db import models
from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='media/courses/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name='картинка', **NULLABLE)
    link = models.URLField(verbose_name='ссылка на видео')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
