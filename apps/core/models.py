"""
Database models.
"""

from django.conf import settings
from django.apps import apps
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from .choices import (
    PRICES,
    UNITS,
)


def get_default_category(group):
    Category = apps.get_model('core', 'Category')
    return Category.objects.get(group=group, name='Other')


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('You must provide a valid email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Brand(models.Model):
    """Cosmetic brand model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    """Group model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='categories')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'group'],
                                    name='unique_category_per_group')
        ]

    def __str__(self):
        return self.name


class Store(models.Model):
    """Store model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='products')
    price = models.CharField(choices=PRICES, default=2, blank=True, null=True)
    ingredients = models.TextField(blank=True)
    capacity = models.FloatField()
    unit = models.CharField(choices=UNITS, default=1)
    stores = models.ManyToManyField(Store, blank=True)
    is_available = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', blank=True)

    def save(self, *args, **kwargs):
        if not self.category:
            self.category = get_default_category(self.group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
