"""
URL mappings for the user API.
"""
from django.urls import path

from .views import UserRegisterView, TokenCreateView


app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('token/', TokenCreateView.as_view(), name='token')
]