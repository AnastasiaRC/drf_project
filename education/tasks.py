from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_mail_update(*args):
    subject = 'Обновление курса'
    message = f'Mатериалы курса "{args[1]}" были обновлены.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [args[0]]
    send_mail(subject, message, from_email, recipient_list)
