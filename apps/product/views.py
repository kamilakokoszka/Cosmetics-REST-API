"""
Views for the product API.
"""
from rest_framework import (
    viewsets,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.core.models import (
    Brand,
)
from . import serializers


class BaseViewSet(viewsets.GenericViewSet):
    """Base viewset for model viewsets."""

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BrandViewSet(BaseViewSet, viewsets.ModelViewSet):
    """Manage Brands in the database."""
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
