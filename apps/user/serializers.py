"""
Serializers for the user API view.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            attrs['user'] = user
            return attrs


class TokenCreateViewResponseSerializer(serializers.Serializer):
    """Serializer for the TokenCreateView response."""
    token = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        fields = '__all__'
