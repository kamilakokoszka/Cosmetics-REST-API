"""
URL mappings for the user API.
"""
from django.urls import include, path
from rest_framework import routers
from .views import (
    BrandViewSet,
    StoreViewSet
)


router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'stores', StoreViewSet, basename='store')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls))
]
