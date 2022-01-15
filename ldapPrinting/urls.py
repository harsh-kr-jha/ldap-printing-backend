
from django.urls import path

from rest_framework import routers
from . import views


urlpatterns = [
    path('auth/', views.authentication, name='auth'),
    path('valid/', views.validate_token, name='auth_valid'),
    path('profile/', views.profile, name='profile'),





]
