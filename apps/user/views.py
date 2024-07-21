"""
Views for the user API.
"""
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    TokenCreateViewResponseSerializer
)


class UserRegisterView(CreateAPIView):
    """Create a new user."""
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


@extend_schema(
    request=AuthTokenSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenCreateViewResponseSerializer
        )
    }
)
class TokenCreateView(ObtainAuthToken):
    """Create a new auth token for user."""

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email
        })
