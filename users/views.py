from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from .utils import email_verification_token, send_verification_email
from rest_framework.views import APIView
User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Вручную проверяем CSRF для API-запросов
        self.check_csrf(request)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'detail': 'Регистрация успешна! Проверьте email для подтверждения.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user, self.request)

    def check_csrf(self, request):
        """
        Кастомная проверка CSRF для API-запросов
        """
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            from django.middleware.csrf import CsrfViewMiddleware
            from django.core.exceptions import PermissionDenied
            
            middleware = CsrfViewMiddleware()
            try:
                middleware.process_view(request, None, (), {})
            except PermissionDenied:
                self.permission_denied(
                    request,
                    message='CSRF проверка не пройдена',
                    code='csrf_failed'
                )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
            if email_verification_token.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'status': 'Email подтверждён!'})
            return Response(
                {'error': 'Неверный токен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]