from celery import shared_task
from .models import UserRecommendation

@shared_task
def update_recommendations_for_all():
    for user in User.objects.all():
        track_ids = hybrid_recommend(user)
        
        # Обновляем рекомендации в БД
        UserRecommendation.objects.filter(user=user).delete()
        for i, track_id in enumerate(track_ids):
            UserRecommendation.objects.create(
                user=user,
                track_id=track_id,
                score=1.0 - (i * 0.05),  # Вес убывает
                source='hybrid'
            )