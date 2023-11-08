from rest_framework import serializers
from education.models import Course, Lesson, Payment, Subscription
from education.services import retrieve_payment, create_payment
from education.validators import VideoValidator
from rest_framework.relations import SlugRelatedField
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator(field='link')]


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    def get_is_subscribed(self, instance):

        if Subscription.objects.filter(course=instance).count() == 0:
            return False
        else:
            return True

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons', 'is_subscribed']


class PaymentSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field="email", queryset=User.objects.all())
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Payment
        fields = "__all__"

    @staticmethod
    def get_course(instance):
        course_value = instance.course
        if course_value:
            try:
                courses = Course.objects.get(title=course_value)
                return str(courses.id)
            except Course.DoesNotExist:
                return "Не найдено"

    @staticmethod
    def get_lesson(instance):
        lesson_value = instance.lesson
        if lesson_value:
            try:
                lessons = Lesson.objects.get(title=lesson_value)
                return str(lessons.id)
            except Lesson.DoesNotExist:
                return "Не найдено"


class PaymentListSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()

    def get_payment_status(self, instance):
        return retrieve_payment(instance.payment_id)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()

    def get_payment_status(self, instance):
        return retrieve_payment(instance.payment_id)

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    def create(self, data):
        data['user'] = self.context['request'].user
        data['payment_id'] = create_payment(int(data.get('amount')))
        payment = Payment.objects.create(**data)
        return payment

    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
