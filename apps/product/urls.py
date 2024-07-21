"""
URL mappings for the user API.
"""
from django.urls import include, path
from rest_framework import routers
from .views import (
    BrandViewSet,
)


router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls))
]
