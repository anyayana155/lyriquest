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
email_verification_token = EmailVerificationTokenGenerator()

def send_verification_email(user, request):
    token = email_verification_token.make_token(user)
    verification_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={
            'uid': user.id,
            'token': token
        })
    )
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
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_welcome_email(user):
    subject = 'Добро пожаловать в Lyriquest!'
    message = f'''
    Поздравляем, {user.username}!

    Ваш email успешно подтверждён, и теперь вы можете 
    пользоваться всеми возможностями Lyriquest.

    Начните путешествие в удивительный мир музыки!

    С уважением,
    Команда Lyriquest
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
# def test_email(): #проверка того, что письма правда отправляются 
#     send_mail(
#         subject='Тестовое письмо',
#         message='Проверка отправки email из LyriQuest!',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=['h8620@yandex.ru'],
#     )