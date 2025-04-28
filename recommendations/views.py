from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

class SimpleRecommendationsAPIView(APIView):
    def get(self, request):
        # Пример: возвращаем 2 случайных трека
        recommended_tracks = [
            {"title": "Yesterday", "artist": "The Beatles", "reason": "Popular"},
            {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "reason": "Trending"},
        ]
        return Response(recommended_tracks)