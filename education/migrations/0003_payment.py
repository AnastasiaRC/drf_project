# Generated by Django 4.2.6 on 2023-10-19 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='дата оплаты')),
                ('amount', models.PositiveIntegerField(verbose_name='сумма оплаты')),
                ('method', models.CharField(choices=[('CARD', 'Наличные'), ('TRANSFER', 'Перевод на счет')], max_length=30, verbose_name='способ оплаты')),
                ('is_paid', models.BooleanField(default=False, verbose_name='статус платежа')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.course', verbose_name='оплаченный курс')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.lesson', verbose_name='оплаченный урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
                'ordering': ['-date'],
            },
        ),
    ]