from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Event, RegistrationCode
from rest_framework import status
from django.test import TestCase

User = get_user_model()

class EventListAPITests(APITestCase):
    def setUp(self):
        code = RegistrationCode.objects.create(code='TESTCODE123')
        self.user = User.objects.create_user(username='testuser', password='testpass123', registration_code=code)
        Event.objects.create(event_title='Teszt Esemény', host='Host1', event_type='Workshop', date='2025-10-10', reward=True, location='Budapest', campfire_link='https://campfire.com/1')
        self.list_url = reverse('event-list')
        self.login_url = reverse('token_obtain_pair')

    def jwt_login(self):
        resp = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(resp.status_code, 200)
        access_token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        self.jwt_login()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event_title'], 'Teszt Esemény')

    def test_detail_unauthenticated(self):
        event = Event.objects.first()
        url = reverse('event-detail', args=[event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_authenticated(self):
        self.jwt_login()
        event = Event.objects.first()
        url = reverse('event-detail', args=[event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event_title'], 'Teszt Esemény')

# Create your tests here.
