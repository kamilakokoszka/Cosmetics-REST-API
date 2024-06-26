"""
Views for the user API.
"""

from rest_framework import generics

from apps.user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer
