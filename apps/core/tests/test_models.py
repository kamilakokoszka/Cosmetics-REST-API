"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='user1@example.com', password='Testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_email_unsuccessful(self):
        """Test creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        """Test creating a superuser is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
