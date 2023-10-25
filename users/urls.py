from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from users.apps import UsersConfig
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
