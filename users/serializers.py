from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Payment
from education.serializers import PaymentListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    user_payment = SerializerMethodField()

    def get_user_payments(self, obj):
        user_payments = Payment.objects.filter(user=obj)
        return PaymentListSerializer(user_payments, many=True).data

    class Meta:
        model = User
        fields = '__all__'
