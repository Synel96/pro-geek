from django.urls import reverse
from rest_framework.test import APITestCase
from core.models import BlogPost, User, RegistrationCode
from rest_framework import status

class BlogPostAPITests(APITestCase):
    def setUp(self):
        self.code = RegistrationCode.objects.create(code='TESTCODE123')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123', first_name='Test', last_name='User', registration_code=self.code)
        self.blog = BlogPost.objects.create(author=self.user, title='Test Blog', preview_image='', created_at='2025-09-30T12:00:00Z')
        self.list_url = reverse('blogpost-list')
        self.detail_url = reverse('blogpost-detail', args=[self.blog.id])
        self.login_url = reverse('token_obtain_pair')

    def jwt_login(self):
        resp = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(resp.status_code, 200)
        access_token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def get_with_auth(self, url):
        return self.client.get(url)

    def post_with_auth(self, url, data):
        return self.client.post(url, data)

    def test_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_unauthenticated(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        self.jwt_login()
        response = self.get_with_auth(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_detail_authenticated(self):
        self.jwt_login()
        response = self.get_with_auth(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_list_wrong_method(self):
        self.jwt_login()
        response = self.post_with_auth(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_not_found(self):
        self.jwt_login()
        url = reverse('blogpost-detail', args=[9999])
        response = self.get_with_auth(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_authenticated_logout(self):
        self.jwt_login()
        logout_url = reverse('token_logout')
        self.client.post(logout_url)
        response = self.get_with_auth(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
