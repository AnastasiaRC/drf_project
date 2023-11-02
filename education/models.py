from django.db import models
from users.models import NULLABLE, User


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


class Payment(models.Model):

    PAYMENT_METHOD = (
        ('CARD', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=30, choices=PAYMENT_METHOD, verbose_name='способ оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='статус платежа')
    payment_id = models.CharField(max_length=100, default='NULL',  verbose_name="id_платежа")

    def __str__(self):
        return f'От {self.user} - {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-date']


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    status = models.BooleanField(default=True, verbose_name='cтатус подписки')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
