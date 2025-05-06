from googleapiclient.discovery import build
from django.conf import settings
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import re

youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

def extract_video_id(url):
    """Извлечение ID видео из URL YouTube"""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
    return None

def search_youtube_tracks(query, max_results=10):
    """Поиск музыкальных треков на YouTube"""
    request = youtube.search().list(
        q=query + " official audio",  # Ищем официальные аудиозаписи
        part="id,snippet",
        maxResults=max_results,
        type="video",
        videoCategoryId="10"  # 10 - категория музыки
    )
    response = request.execute()
    
    tracks = []
    for item in response['items']:
        video_id = item['id']['videoId']
        snippet = item['snippet']
        
        # Очистка названия (удаляем "Official Audio" и т.п.)
        title = re.sub(r'(official\s*(audio|video|lyrics)?|lyrics|ft\.?.*)$', '', 
                      snippet['title'], flags=re.IGNORECASE).strip()
        
        tracks.append({
            'youtube_id': video_id,
            'title': title,
            'artist': snippet.get('channelTitle', '').replace(' - Topic', ''),
            'thumbnail_url': snippet['thumbnails']['high']['url'],
            'published_at': snippet['publishedAt'],
            'url': f'https://www.youtube.com/watch?v={video_id}'
        })
    
    return tracks

def get_audio_stream_url(youtube_url):
    """Получение URL аудиопотока через pytube"""
    try:
        yt = YouTube(youtube_url)
        # Пробуем получить поток с самым высоким битрейтом
        stream = yt.streams.filter(only_audio=True).order_by('abr').last()
        
        if not stream:
            # Если не нашли аудио поток, пробуем любой поток
            stream = yt.streams.first()
            
        if stream:
            print(f"Found stream: {stream}")
            return stream.url
        return None
    except Exception as e:
        print(f"Error getting audio stream: {str(e)}")
        return None

    