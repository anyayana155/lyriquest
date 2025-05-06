from rest_framework import serializers
from .models import Track, Emotion

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class TrackSerializer(serializers.ModelSerializer):
    emotions = EmotionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Track
        fields = [
            'id', 'youtube_id', 'title', 'artist', 
            'duration', 'thumbnail_url', 'play_count',
            'emotions'
        ]