from rest_framework import generics, status
from rest_framework.response import Response
from .models import Track, Emotion
from .serializers import MusicTrackSerializer, EmotionSerializer

class EmotionListCreate(generics.ListCreateAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

class MusicTrackListCreate(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = MusicTrackSerializer

class MusicTrackRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = MusicTrackSerializer

#Пример добавления эмоций к треку
class MusicTrackAddEmotion(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = MusicTrackSerializer

    def patch(self, request, *args, **kwargs):
        track = self.get_object()
        emotion_id = request.data.get('emotion_id')

        try:
            emotion = Emotion.objects.get(pk=emotion_id)
        except Emotion.DoesNotExist:
            return Response({'error': 'Emotion not found'}, status=status.HTTP_400_BAD_REQUEST)

        track.emotions.add(emotion)
        serializer = self.get_serializer(track)
        return Response(serializer.data)