from django.urls import path
from education.views import CourseViewSet, PaymentListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView, \
    CourseCreateViewSet, CourseRetrieveViewSet, CourseUpdateViewSet, CourseDeleteViewSet, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, PaymentDeleteView
from education.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView
from rest_framework.routers import DefaultRouter
from education.apps import EducationConfig

app_name = EducationConfig.name

router = DefaultRouter()
# router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete'),

    path('course/', CourseViewSet.as_view({'get': 'list'}), name='course_list'),
    path('course/create/', CourseCreateViewSet.as_view({'post': 'create'}), name='course_create'),
    path('course/<int:pk>/', CourseRetrieveViewSet.as_view({'get': 'retrieve'}),name='course_detail'),
    path('course/update/<int:pk>/', CourseUpdateViewSet.as_view({'put': 'update'}),name='course_update'),
    path('course/delete/<int:pk>/', CourseDeleteViewSet.as_view({'delete': 'destroy'}),name='course_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
    path('payment/delete/<int:pk>/', PaymentDeleteView.as_view(),name='payment_delete'),

    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),

] + router.urls

