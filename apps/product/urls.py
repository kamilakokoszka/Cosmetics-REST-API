"""
URL mappings for the user API.
"""
from django.urls import include, path
from rest_framework import routers
from .views import (
    BrandViewSet,
    StoreViewSet,
    GroupViewSet,
    CategoryViewSet,
)


router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'groups', GroupViewSet, basename='group')


app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
    path('groups/<int:group_id>/categories/',
         CategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='category-list'),
    path('groups/<int:group_id>/categories/<int:pk>/',
         CategoryViewSet.as_view({'get': 'retrieve',
                                  'put': 'update',
                                  'delete': 'destroy'}),
         name='category-detail'),
]
