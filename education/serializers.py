from rest_framework import serializers
from education.models import Course, Lesson, Payment
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

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field="email", queryset=User.objects.all())
    course = serializers.SerializerMethodField(read_only=True)
    lesson = serializers.SerializerMethodField(read_only=True)

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
