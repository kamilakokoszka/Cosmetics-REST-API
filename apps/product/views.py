"""
Views for the product API.
"""
from rest_framework import (
    viewsets,
    generics
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.core.models import (
    Brand,
    Store,
    Group,
    Category,
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


class StoreViewSet(BaseViewSet, viewsets.ModelViewSet):
    """Manage Stores in the database."""
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """List all groups and retrieve a single group with its categories."""
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).prefetch_related('categories').order_by('-name').distinct()


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories in the database."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        queryset = self.queryset
        group_id = self.kwargs.get('group_id')
        return queryset.filter(
            user=self.request.user,
            group_id=group_id
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Customize the creation process to assign
        the category to a specific group."""
        group_id = self.kwargs.get('group_id')
        group = generics.get_object_or_404(Group, id=group_id)
        serializer.save(user=self.request.user, group=group)
