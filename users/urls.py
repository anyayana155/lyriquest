app_name = 'users'  # Добавляем app_name для namespace

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, VerifyEmailView, CustomTokenObtainPairView  # Используем CustomTokenObtainPairView вместо LoginView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Изменено с LoginView
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]