from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from .utils import email_verification_token, send_verification_email

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user, self.request)

class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
            if email_verification_token.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'status': 'Email подтверждён!'})
            return Response({'error': 'Неверный токен'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer