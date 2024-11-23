"""
Tests for the category API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Category, Group
from apps.product.serializers import CategorySerializer


def category_list_url(group_id):
    """Create and return a group with categories listed URL."""
    return reverse('product:category-list', args=[group_id])


def category_detail_url(group_id, category_id):
    """Create and return a category detail URL."""
    return reverse('product:category-detail', args=[group_id, category_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_category_view_auth_required(self):
        """Test auth is required to call API."""
        url = category_list_url(group_id=1)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryApiTests(TestCase):
    """Tests for the category API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com',
                                username='Testuser',
                                password='Testpass123')
        self.client.force_authenticate(self.user)
        self.group = Group.objects.create(name='Test Group', user=self.user)

    def test_create_category(self):
        """Test creating a category."""
        payload = {
            'name': 'Test category'
        }
        url = category_list_url(self.group.id)
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        category = Category.objects.filter(group=self.group).first()
        self.assertEqual(Category.objects.count(), 5)   # 4 categories are already created with User creation
        self.assertEqual(category.name, payload['name'])
        self.assertEqual(category.group, self.group)

    def test_get_category_detail(self):
        """Test get category details with list of products
        belonging to it."""                             # TO-DO: products
        category = Category.objects.create(name='Test category',
                                           user=self.user,
                                           group=self.group)

        self.assertIsNotNone(category)

        url = category_detail_url(self.group.id, category.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = CategorySerializer(category)
        self.assertEqual(res.data, serializer.data)

    def test_update_category(self):
        """Test update of a category."""
        category = Category.objects.create(name='Test category',
                                           user=self.user,
                                           group=self.group)

        self.assertIsNotNone(category)

        payload = {'name': 'Test category 2'}
        url = category_detail_url(self.group.id, category.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        category.refresh_from_db()

        self.assertEqual(category.name, payload['name'])
        self.assertEqual(category.user, self.user)

    def test_delete_category(self):
        """Test deleting a category successful."""
        category = Category.objects.create(name='Test category',
                                           user=self.user,
                                           group=self.group)

        self.assertIsNotNone(category)

        url = category_detail_url(self.group.id, category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_delete_other_user_category_error(self):
        """Test trying to delete another user category gives an error."""
        another_user = create_user(email='test2@example.com',
                                   username='Testuser2',
                                   password='Testpass456')
        another_user_group = Group.objects.get(name='Skin care',
                                               user=another_user)
        category = Category.objects.create(name='Test category',
                                           user=another_user,
                                           group=another_user_group)

        self.assertIsNotNone(another_user_group)
        self.assertIsNotNone(category)

        url = category_detail_url(another_user_group.id, category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Category.objects.filter(id=category.id).exists())
