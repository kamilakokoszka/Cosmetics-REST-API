"""
Serializers for the user API view.
"""

from rest_framework import serializers
from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)

