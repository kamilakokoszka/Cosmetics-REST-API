"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:user-register')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class UserApiTests(TestCase):
    """Tests for the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error returned if password less than 5 characters."""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'tp'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


class AuthTokenTests(TestCase):
    """Tests for the auth token API"""

    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'Testpass123'
        self.user = create_user(username=self.username,
                                email=self.email,
                                password=self.password)

    def test_obtain_token_success(self):
        """Test token is obtained with valid credentials."""
        payload = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        self.assertEqual(res.data['email'], self.user.email)

    def test_obtain_token_invalid_credentials(self):
        """Test token is not obtained with invalid credentials."""
        payload = {
            'username': self.username,
            'email': self.email,
            'password': 'pass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_obtain_token_missing_credentials(self):
        """Test token is not obtained with missing credentials."""
        payload = {
            'username': self.username,
            'email': self.email,
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_get_method_not_allowed(self):
        """Test GET method is not allowed."""
        res = self.client.get(TOKEN_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
