from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, DestroyAPIView
from education.models import Course, Lesson, Payment
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # def perform_create(self, serializer):
    #     course = serializer.save()
    #     course.author = self.request.user
    #     course.save()

    # def list(self, request):
    #     if self.request.user.is_manager:
    #         queryset = Course.objects.all()
    #     else:
    #         queryset = Course.objects.filter(author=self.request.user)
    #     return queryset


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     lesson = serializer.save()
    #     lesson.author = self.request.user
    #     lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_moderator:
    #         queryset = Lesson.objects.all()
    #     else:
    #         queryset = Lesson.objects.filter(author=self.request.user)
    #     return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date', 'method', 'course', 'lesson']
    ordering_fields = ('date',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
