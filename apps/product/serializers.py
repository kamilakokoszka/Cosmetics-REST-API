"""
Serializers for the product API view.
"""
from rest_framework import serializers

from apps.core.models import (
    Brand,
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for brand."""

    class Meta:
        model = Brand
        fields = ['id', 'name']
        read_only_fields = ['id']
