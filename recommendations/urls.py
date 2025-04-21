from django.urls import path
from .views import SimpleRecommendationsAPIView

urlpatterns = [path('', SimpleRecommendationsAPIView.as_view()),
]