from collections import defaultdict
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from music.models import Track
def collaborative_filtering(user, limit=10):
    liked_tracks = user.liked_tracks.values_list('id', flat=True)
    similar_users = User.objects.filter(
        liked_tracks__in=liked_tracks
    ).exclude(id=user.id).annotate(
        common_tracks=Count('liked_tracks')
    ).order_by('-common_tracks')[:100]
    track_scores = defaultdict(float)
    for sim_user in similar_users:
        for track in sim_user.liked_tracks.exclude(id__in=liked_tracks):
            track_scores[track.id] += 1 / (1 + sim_user.common_tracks)
    sorted_tracks = sorted(track_scores.items(), key=lambda x: -x[1])
    return [track_id for track_id, score in sorted_tracks[:limit]]


def content_based_recommend(user, limit=10):
    liked_genres = list(user.liked_tracks.values_list('genres__name', flat=True))
    all_tracks = Track.objects.all()
    genre_texts = [" ".join(t.genres.values_list('name', flat=True)) for t in all_tracks]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(genre_texts)
    user_vector = vectorizer.transform([" ".join(liked_genres)])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    recommended_indices = similarities.argsort()[-limit:][::-1]
    return [all_tracks[i].id for i in recommended_indices]
def hybrid_recommend(user, limit=10):
    collab_tracks = collaborative_filtering(user, limit//2)
    content_tracks = content_based_recommend(user, limit//2)
    combined = list(set(collab_tracks + content_tracks))
    return sorted(combined, key=lambda x: Track.objects.get(id=x).likes.count(), reverse=True)[:limit]