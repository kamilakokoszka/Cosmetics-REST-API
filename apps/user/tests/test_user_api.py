"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:user-register')


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
