from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        'auth': request.build_absolute_uri('auth/'),
        'music': request.build_absolute_uri('music/')
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/auth/', include(('users.urls', 'users'), namespace='auth-api')),  # Исправленный include
    path('api/music/', include('music.urls')),
    
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('auth/', TemplateView.as_view(template_name='regaut.html'), name='auth'),
    path('regaut/', TemplateView.as_view(template_name='regaut.html'), name='regaut'),
    path('music/', TemplateView.as_view(template_name='music.html'), name='music'),
    path('profile/', TemplateView.as_view(template_name='index.html'), name='profile'),
    
    # Для обратной совместимости
    path('home.html', TemplateView.as_view(template_name='home.html')),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('music.html', TemplateView.as_view(template_name='music.html')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)