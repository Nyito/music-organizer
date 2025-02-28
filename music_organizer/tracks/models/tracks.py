from django.db import models

class Track(models.Model):
    spotify_id = models.TextField(unique=True)
    name = models.TextField()
    album = models.TextField(null=True)
    artist = models.TextField()
    duration_ms = models.TextField()
    url = models.URLField(null=True)
    added_at = models.DateField(null=True)
