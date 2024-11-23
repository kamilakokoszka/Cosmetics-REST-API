"""
Tests for the group APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Group, Category
from apps.product.serializers import GroupSerializer


GROUP_LIST_URL = reverse('product:group-list')


def group_detail_url(group_id):
    """Create and return a group detail URL."""
    return reverse('product:group-detail', args=[group_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_group_view_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(GROUP_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class GroupApiTests(TestCase):
    """Tests for the group API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com',
                                username='Testuser',
                                password='Testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_groups(self):
        """Test retrieving a list of groups."""

        res = self.client.get(GROUP_LIST_URL)

        groups = Group.objects.all().order_by('-name')
        serializer = GroupSerializer(groups, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_group_not_possible(self):
        """Test creating a group is not possible."""
        payload = {
            'name': 'Test group'
        }
        res = self.client.post(GROUP_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        group = Group.objects.filter(name=payload['name'])
        self.assertFalse(group)

    def test_get_group_detail(self):
        """Test get group details with categories belonging to it."""
        group = Group.objects.get(name='Skin care', user=self.user)
        Category.objects.create(name='Category 1', group=group, user=self.user)
        Category.objects.create(name='Category 2', group=group, user=self.user)

        url = group_detail_url(group.id)
        res = self.client.get(url)

        serializer = GroupSerializer(group)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_group_forbidden(self):
        """Test update of a group is not allowed."""
        group = Group.objects.get(name='Skin care')
        payload = {
            'name': 'Test group 1'
        }
        url = group_detail_url(group.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        group.refresh_from_db()
        self.assertEqual(group.name, 'Skin care')

    def test_delete_group_forbidden(self):
        """Test deleting a group is not allowed."""
        group = Group.objects.get(name='Skin care')

        url = group_detail_url(group.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Group.objects.filter(id=group.id).exists())
