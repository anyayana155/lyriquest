from django.db import models
from users.models import User

class Emotion(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Track(models.Model):
    # Основная информация
    youtube_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    duration = models.IntegerField(default=0)  # в секундах
    
    # Метаданные
    thumbnail_url = models.URLField(max_length=500)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Связи
    emotions = models.ManyToManyField(Emotion, related_name='tracks', blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Статистика
    play_count = models.PositiveIntegerField(default=0)
    last_played = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist or 'Unknown'}"

    class Meta:
        db_table = 'music_track'
        ordering = ['-last_played']
