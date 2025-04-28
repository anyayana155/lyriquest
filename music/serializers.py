from rest_framework import serializers
from .models import Track, Emotion

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class MusicTrackSerializer(serializers.ModelSerializer):
    emotions = EmotionSerializer(many=True, read_only=True) # Вложенный сериализатор для эмоций

    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'audio_file', 'artwork', 'emotions']