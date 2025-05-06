from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Track, Emotion
from .serializers import TrackSerializer, EmotionSerializer
from .services import search_youtube_tracks, get_audio_stream_url
from django.http import JsonResponse
class YouTubeSearchView(APIView):
    """Поиск треков через YouTube API"""
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)
        
        tracks = search_youtube_tracks(query)
        return Response(tracks)

class YouTubeAudioView(APIView):
    def get(self, request):
        video_id = request.query_params.get('id', '')
        if not video_id:
            return Response({"error": "Video ID is required"}, status=400)
        
        youtube_url = f'https://www.youtube.com/watch?v={video_id}'
        print(f"Fetching audio for: {youtube_url}")  # Логируем URL
        
        audio_url = get_audio_stream_url(youtube_url)
        print(f"Audio URL: {audio_url}")  # Логируем полученный URL
        
        if not audio_url:
            return Response({"error": "Could not get audio stream"}, status=400)
            
        return Response({"audio_url": audio_url})

class TrackListView(generics.ListCreateAPIView):
    """Список треков в локальной БД"""
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали трека"""
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class EmotionListView(generics.ListAPIView):
    """Список эмоций"""
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
