from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from education.models import Course, Lesson, Payment
from education.paginators import Pagination
from education.permissions import IsOwner, IsModerator, IsMember
from education.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, \
    SubscriptionSerializer, PaymentRetrieveSerializer, PaymentCreateSerializer, PaymentListSerializer, \
    PaymentSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, DestroyAPIView
from education.tasks import send_mail_update


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class CourseCreateViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        course = serializer.save()
        course.author = self.request.user
        course.save()


class CourseUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner | IsModerator]

    def perform_update(self, serializer):
        instance = serializer.save()
        user = self.request.user
        user_email = user.email
        course_name = instance.title
        send_mail_update.delay(user_email, course_name)


class CourseRetrieveViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner | IsModerator]


class CourseDeleteViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsOwner | IsMember]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.author = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDeleteAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsMember]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date', 'method', 'course', 'lesson']
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentDeleteView(DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
