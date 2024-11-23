"""
Serializers for the product API view.
"""
from rest_framework import serializers

from apps.core.models import (
    Brand,
    Store,
    Group,
    Category,
    Product,
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for brand."""

    class Meta:
        model = Brand
        fields = ['id', 'name']
        read_only_fields = ['id']


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for store."""

    class Meta:
        model = Store
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product."""

    class Meta:
        model = Product
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""
    # products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'group']
        read_only_fields = ['id']
        extra_kwargs = {
            'group': {'required': False},
        }


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for group."""
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'categories']
        read_only_fields = ['id']
