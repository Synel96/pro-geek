from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class CoreSecurityTests(APITestCase):
    def test_blog_list_requires_auth(self):
        url = reverse('blogpost-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_news_list_requires_auth(self):
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_events_list_requires_auth(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_csrf_protection_on_post(self):
        url = reverse('blogpost-list')
        response = self.client.post(url, {'title': 'Test'}, format='json')
        # 403 Forbidden, ha nincs CSRF token
        self.assertIn(response.status_code, [401, 403])

    def test_invalid_jwt_token(self):
        url = reverse('blogpost-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
