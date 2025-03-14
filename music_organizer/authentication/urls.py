# authentication/urls.py
from django.urls import path
from .views import dashboard_view
from .views import SpotifyViewSet

urlpatterns = [
    path('callback/', SpotifyViewSet.as_view({'get': 'callback'}), name='spotify_callback'),
    path('dashboard/', dashboard_view, name='dashboard'), # Add this line
]
