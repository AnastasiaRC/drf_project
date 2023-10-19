from django.core.management import BaseCommand
from education.models import Payment
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()
        with open("pay_data.json", "r", encoding='utf8') as file:
            payments = json.load(file)
            for payment in payments:
                user = payment['fields']['user']
                date = payment['fields']['date']
                course = payment['fields']['course']
                lesson = payment['fields']['lesson']
                amount = payment['fields']['amount']
                method = payment['fields']['method']

                Payment.objects.create(user_id=user, date=date, course_id=course, lesson_id=lesson, amount=amount, method=method)
