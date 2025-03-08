from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="spotify_token")
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateField()
