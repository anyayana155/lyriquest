from django.db import models
from users.models import User
class Emotion(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='music/audio/')
    artwork = models.ImageField(upload_to='music/artwork/', blank=True, null=True)
    emotions = models.ManyToManyField(Emotion, related_name='tracks', blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

    class Meta:
        db_table = 'music_track'