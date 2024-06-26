"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import (
    Brand,
    Group,
    Category,
    Store,
    Product
)


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

    def test_create_brand(self):
        """Test creating a brand is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )
        brand = Brand.objects.create(
            user=user,
            name='Test brand',
        )

        self.assertEqual(str(brand), brand.name)

    def test_create_group(self):
        """Test creating a group is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )
        group = Group.objects.create(
            user=user,
            name='Test group',
        )

        self.assertEqual(str(group), group.name)

    def test_create_category(self):
        """Test creating a category is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )
        group = Group.objects.create(
            user=user,
            name='Test group',
        )
        category = Category.objects.create(
            user=user,
            name='Test category',
            group=group
        )

        self.assertEqual(str(category), category.name)
        self.assertEqual(category.group.name, group.name)

    def test_create_store(self):
        """Test creating a store is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )
        store = Store.objects.create(
            user=user,
            name='Test store'
        )

        self.assertEqual(str(store), store.name)

    def test_create_product(self):
        """Test creating a product is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123',
        )
        brand = Brand.objects.create(
            user=user,
            name='Test brand',
        )
        group = Group.objects.create(
            user=user,
            name='Test group',
        )
        category = Category.objects.create(
            user=user,
            name='Test category',
            group=group
        )
        store = Store.objects.create(
            user=user,
            name='Test store'
        )
        product = Product.objects.create(
            user=user,
            name='Test product',
            brand=brand,
            group=group,
            category=category,
            price=15.00,
            ingredients='Test, test, test',
            capacity=50,
            unit=2,
            is_available=True,
            is_favourite=False
        )
        product.stores.add(store)

        self.assertEqual(str(product), product.name)
        self.assertEqual(product.brand.name, brand.name)
        self.assertEqual(product.category.group.name, group.name)
