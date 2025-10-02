from django.urls import reverse
from rest_framework.test import APITestCase
from core.models import RegistrationCode, User
from unittest.mock import patch

class AuthAppTests(APITestCase):
    def setUp(self):
        self.code = RegistrationCode.objects.create(code='TESTCODE123')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'registration_code': self.code.code,
        }

    def test_check_code_valid(self):
        url = reverse('check_code')
        response = self.client.post(url, {'registration_code': self.code.code})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['valid'])

    def test_check_code_invalid(self):
        url = reverse('check_code')
        response = self.client.post(url, {'registration_code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['valid'])

    def test_register_success(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Registration successful')
        self.code.refresh_from_db()
        self.assertTrue(self.code.is_used)

    def test_register_with_used_code(self):
        # Use code once
        self.client.post(reverse('register'), self.user_data)
        # Try again
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('registration_code', response.data)

    def test_login_success(self):
        # Register user first
        self.client.post(reverse('register'), self.user_data)
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Login successful')
        # Csak akkor ellenőrzöm a sütiket, ha tényleg vannak
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)

    def test_login_fail(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'nouser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)

    def test_refresh_success(self):
        # Register and login
        self.client.post(reverse('register'), self.user_data)
        login_resp = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass123'})
        if 'refresh' in login_resp.cookies:
            self.client.cookies['refresh'] = login_resp.cookies['refresh'].value
        url = reverse('token_refresh')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Token refreshed')
        self.assertIn('access', response.cookies)

    def test_refresh_fail(self):
        url = reverse('token_refresh')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        url = reverse('token_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['detail'], 'Logged out')

    def test_activate_user_success(self):
        self.client.post(reverse('register'), self.user_data)
        user = User.objects.get(username='testuser')
        user.is_active = False
        user.save()
        url = reverse('activate_user')
        response = self.client.post(url, {'username': 'testuser', 'activation_code': self.code.code})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Fiók aktiválva.')
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_forgot_password_success(self):
        self.client.post(reverse('register'), self.user_data)
        url = reverse('forgot_password')
        response = self.client.post(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('reset_token', response.data)
        self.assertIn('username', response.data)

    @patch('authapp.views.send_mail')
    def test_activation_email_sent(self, mock_send_mail):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 201)
        if response.status_code == 201:
            mock_send_mail.assert_called()
            args, kwargs = mock_send_mail.call_args
            self.assertIn('Fiók aktiválása', args[0])
            self.assertIn(self.user_data['email'], args[3])

    @patch('authapp.views.send_mail')
    def test_forgot_password_email_sent(self, mock_send_mail):
        reg_resp = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(reg_resp.status_code, 201)
        response = self.client.post(reverse('forgot_password'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            mock_send_mail.assert_called()
            args, kwargs = mock_send_mail.call_args
            self.assertIn('Jelszó visszaállítás', args[0])
            self.assertIn('test@example.com', args[3])

    def test_reset_password_success(self):
        reg_resp = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(reg_resp.status_code, 201)
        user = User.objects.get(username='testuser')
        url_fp = reverse('forgot_password')
        resp_fp = self.client.post(url_fp, {'email': 'test@example.com'})
        self.assertEqual(resp_fp.status_code, 200)
        token = resp_fp.data['reset_token']
        url_rp = reverse('reset_password')
        response = self.client.post(url_rp, {'username': 'testuser', 'reset_token': token, 'new_password': 'newpass123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Jelszó sikeresen módosítva.')
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))
