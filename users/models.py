from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    favorite_artists = models.JSONField(default=list)
    disliked_artists = models.JSONField(default=list)
    liked_tracks = models.JSONField(default=list)
    disliked_tracks = models.JSONField(default=list)
    
    def __str__(self):
        return self.username