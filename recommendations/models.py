from django.db import models
from users.models import User
from music.models import Track

class UserRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)  # Вес рекомендации (0.0-1.0)
    source = models.CharField(max_length=50)  # 'collab', 'content', 'hybrid'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'track']]