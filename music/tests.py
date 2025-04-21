from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import MusicTrack, Emotion

class MusicTests(APITestCase):
    def test_create_music_track(self):
        """
        Ensure we can create a new music track object.
        """
        url = reverse('musictrack-list-create')
        data = {'title': 'Test Track', 'artist': 'Test Artist'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MusicTrack.objects.count(), 1)
        self.assertEqual(MusicTrack.objects.get().title, 'Test Track')

    def test_get_music_track(self):
        """
        Ensure we can get a music track object.
        """
        track = MusicTrack.objects.create(title='Test Track', artist='Test Artist')
        url = reverse('musictrack-retrieve-update-destroy', args=[track.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Track')

    def test_create_emotion(self):
        """
        Ensure we can create a new emotion object.
        """
        url = reverse('emotion-list-create')
        data = {'name': 'Happy'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Emotion.objects.count(), 1)
        self.assertEqual(Emotion.objects.get().name, 'Happy')