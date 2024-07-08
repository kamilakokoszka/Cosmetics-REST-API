"""
Views for the user API.
"""

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from apps.user.serializers import UserSerializer


class UserRegisterView(CreateAPIView):
    """Create a new user."""
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
