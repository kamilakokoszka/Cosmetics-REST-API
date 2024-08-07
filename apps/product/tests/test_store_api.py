"""
Tests for the store API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Store
from apps.product.serializers import StoreSerializer


STORE_LIST_URL = reverse('product:store-list')


def store_detail_url(store_id):
    """Create and return a store detail URL."""
    return reverse('product:store-detail', args=[store_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_store_view_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(STORE_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class StoreApiTests(TestCase):
    """Tests for the store API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com',
                                username='Testuser',
                                password='Testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_stores(self):
        """Test retrieving a list of stores."""
        Store.objects.create(name='Test store', user=self.user)
        Store.objects.create(name='Test store', user=self.user)

        res = self.client.get(STORE_LIST_URL)

        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_store_list_limited_to_user(self):
        """Test list of stores is limited to authenticated user."""
        other_user = create_user(email='test2@example.com',
                                 username='Testuser2',
                                 password='Testpass456')
        Store.objects.create(name='Test store', user=self.user)
        Store.objects.create(name='Test store', user=other_user)

        res = self.client.get(STORE_LIST_URL)

        stores = Store.objects.filter(user=self.user)
        serializer = StoreSerializer(stores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_store(self):
        """Test creating a store."""
        payload = {
            'name': 'Test store'
        }
        res = self.client.post(STORE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        store = Store.objects.first()
        self.assertEqual(store.user, self.user)

    def test_get_store_detail(self):
        """Test get store details."""
        store = Store.objects.create(name='Test store', user=self.user)

        url = store_detail_url(store.id)
        res = self.client.get(url)

        serializer = StoreSerializer(store)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_store(self):
        """Test update of a store."""
        store = Store.objects.create(name='Test store', user=self.user)
        payload = {
            'name': 'Test store 2'
        }
        url = store_detail_url(store.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        store.refresh_from_db()
        self.assertEqual(store.name, payload['name'])
        self.assertEqual(store.user, self.user)

    def test_delete_store(self):
        """Test deleting a store successful."""
        store = Store.objects.create(name='Test store', user=self.user)

        url = store_detail_url(store.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Store.objects.filter(id=store.id).exists())

    def test_delete_other_user_store_error(self):
        """Test trying to delete another user store gives an error."""
        another_user = create_user(email='test2@example.com',
                                   username='Testuser2',
                                   password='Testpass456')
        store = Store.objects.create(name='Test store', user=another_user)

        url = store_detail_url(store.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Store.objects.filter(id=store.id).exists())
