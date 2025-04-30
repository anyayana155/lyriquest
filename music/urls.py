from django.urls import path
from .views import MusicTrackListCreate, MusicTrackRetrieveUpdateDestroy, EmotionListCreate, MusicTrackAddEmotion, MusicListView

urlpatterns = [
    path('emotions/', EmotionListCreate.as_view(), name='emotion-list-create'),
    path('tracks/', MusicTrackListCreate.as_view(), name='musictrack-list-create'),
    path('tracks/<int:pk>/', MusicTrackRetrieveUpdateDestroy.as_view(), name='musictrack-retrieve-update-destroy'),
    path('tracks/<int:pk>/add_emotion/', MusicTrackAddEmotion.as_view(), name='musictrack-add-emotion'), #Добавление эмоции к треку
    path('', MusicListView.as_view(), name='music-list'),
]