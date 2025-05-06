from django.urls import path
from .views import (
    YouTubeSearchView,
    YouTubeAudioView,
    TrackListView,
    TrackDetailView,
    EmotionListView
)

urlpatterns = [
    # YouTube API
    path('youtube/search/', YouTubeSearchView.as_view(), name='youtube-search'),
    path('youtube/audio/', YouTubeAudioView.as_view(), name='youtube-audio'),
    
    # Локальные данные
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('emotions/', EmotionListView.as_view(), name='emotion-list'),
]
