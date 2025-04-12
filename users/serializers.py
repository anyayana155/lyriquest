from rest_framework import serializers
from .models import User  

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password',
            'favorite_artists',
            'disliked_artists',
            'liked_tracks',
            'disliked_tracks'
        ]
        extra_kwargs = {
            'favorite_artists': {'required': False},
            'disliked_artists': {'required': False},
            'liked_tracks': {'required': False},
            'disliked_tracks': {'required': False}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            favorite_artists=validated_data.get('favorite_artists', []),
            disliked_artists=validated_data.get('disliked_artists', []),
            liked_tracks=validated_data.get('liked_tracks', []),
            disliked_tracks=validated_data.get('disliked_tracks', [])
        )
        return user