"""
Tests for the brand API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Brand
from apps.product.serializers import BrandSerializer


BRAND_LIST_URL = reverse('product:brand-list')


def brand_detail_url(brand_id):
    """Create and return a brand detail URL."""
    return reverse('product:brand-detail', args=[brand_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_brand_view_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BRAND_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class BrandApiTests(TestCase):
    """Tests for the brand API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com',
                                username='Testuser',
                                password='Testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_brands(self):
        """Test retrieving a list of stores."""
        Brand.objects.create(name='Test brand', user=self.user)
        Brand.objects.create(name='Test brand', user=self.user)

        res = self.client.get(BRAND_LIST_URL)

        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_brand_list_limited_to_user(self):
        """Test list of brands is limited to authenticated user."""
        other_user = create_user(email='test2@example.com',
                                 username='Testuser2',
                                 password='Testpass456')
        Brand.objects.create(name='Test brand', user=self.user)
        Brand.objects.create(name='Test brand', user=other_user)

        res = self.client.get(BRAND_LIST_URL)

        brands = Brand.objects.filter(user=self.user)
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_brand(self):
        """Test creating a brand."""
        payload = {
            'name': 'Test brand'
        }
        res = self.client.post(BRAND_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        brand = Brand.objects.first()
        self.assertEqual(brand.user, self.user)

    def test_get_brand_detail(self):
        """Test get brand details."""
        brand = Brand.objects.create(name='Test brand', user=self.user)

        url = brand_detail_url(brand.id)
        res = self.client.get(url)

        serializer = BrandSerializer(brand)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_brand(self):
        """Test update of a brand."""
        brand = Brand.objects.create(name='Test brand', user=self.user)
        payload = {
            'name': 'Test brand 2'
        }
        url = brand_detail_url(brand.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        brand.refresh_from_db()
        self.assertEqual(brand.name, payload['name'])
        self.assertEqual(brand.user, self.user)

    def test_delete_brand(self):
        """Test deleting a brand successful."""
        brand = Brand.objects.create(name='Test brand', user=self.user)

        url = brand_detail_url(brand.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Brand.objects.filter(id=brand.id).exists())

    def test_delete_other_user_brand_error(self):
        """Test trying to delete another user brand gives an error."""
        another_user = create_user(email='test2@example.com',
                                   username='Testuser2',
                                   password='Testpass456')
        brand = Brand.objects.create(name='Test brand', user=another_user)

        url = brand_detail_url(brand.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Brand.objects.filter(id=brand.id).exists())
