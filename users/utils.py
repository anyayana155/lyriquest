from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +  
            str(timestamp) +
            str(user.is_active)
        )

# Экземпляр генератора для использования в других модулях
email_verification_token = EmailVerificationTokenGenerator()

def send_verification_email(user, request):
    # Генерируем уникальный токен
    token = email_verification_token.make_token(user)
    
    # Строим URL для подтверждения
    verification_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={
            'uid': user.id,
            'token': token
        })
    )
    
    # Формируем письмо
    subject = 'Подтверждение email для Lyriquest'
    message = f'''
    Здравствуйте, {user.username}!

    Для завершения регистрации на Lyriquest, пожалуйста, 
    подтвердите ваш email, перейдя по ссылке:

    {verification_url}

    Если вы не регистрировались на нашем сервисе, 
    просто проигнорируйте это письмо.

    Спасибо,
    Команда Lyriquest
    '''
    
    # Отправляем письмо
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_welcome_email(user):
    """
    Отправляет приветственное письмо после подтверждения email.
    """
    subject = 'Добро пожаловать в Lyriquest!'
    message = f'''
    Поздравляем, {user.username}!

    Ваш email успешно подтверждён, и теперь вы можете 
    пользоваться всеми возможностями Lyriquest.

    Начните путешествие в удивительный мир музыки музыку!

    С уважением,
    Команда Lyriquest
    '''
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )