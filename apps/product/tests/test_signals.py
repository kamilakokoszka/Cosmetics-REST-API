"""
Tests for signals.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core.models import Group


def create_user(email='user1@example.com', password='Testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class SignalsTests(TestCase):
    """Test signals."""

    def test_groups_created_when_user_created(self):
        """Test groups are created when user is created."""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        group_names = (Group.objects.filter(user=user)
                       .values_list('name', flat=True))

        expected_group_names = [
            "Skin care",
            "Hair care",
            "Body care",
            "Makeup",
            "Other"
        ]

        self.assertEqual(list(group_names), expected_group_names)

    def test_categories_for_groups_created(self):
        """Test 'Other' category created for each group except 'Other'"""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        groups = Group.objects.filter(user=user).exclude(name='Other')
        for group in groups:
            category = group.categories.first()
            self.assertEqual(category.name, 'Other')
