"""
URL mappings for the user API.
"""
from django.urls import path

from .views import UserRegisterView


app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register')
]