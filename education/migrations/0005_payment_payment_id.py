# Generated by Django 4.2.6 on 2023-11-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default='NULL', max_length=100, verbose_name='id_платежа'),
        ),
    ]
