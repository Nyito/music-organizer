import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from django.conf import settings
from authentication.models.spotify_token import SpotifyToken
from django.utils import timezone


class SpotifyConnector:
    def __init__(self, scope, user):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_url = settings.SPOTIFY_REDIRECT_URL
        self.scope = scope
        self.user = user
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_url,
            scope=self.scope,
        )

    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()
    
    def handle_callback(self, code):
        token = self.sp_oauth.get_access_token(code)
        access_token = token['access_token']
        refresh_token = token.get('refresh_token')
        expires_in = token.get('expires_in', 3600)

        expiry_datetime = timezone.now() + timezone.timedelta(seconds=expires_in)

        return access_token, refresh_token, expiry_datetime
    
    def save_tokens(self, access_token, refresh_token, expiry_datetime):
        spotify_token, created = SpotifyToken.objects.get_or_create(user=self.user)
        spotify_token.access_token = access_token
        spotify_token.refresh_token = refresh_token
        spotify_token.expires_at = expiry_datetime
        spotify_token.save()

    def get_access_token(self):
        try:
            spotify_token = SpotifyToken.objects.get(user=self.user)
            if spotify_token.is_token_expired():
                self.refresh_access_token()  # Refresh if expired
            return spotify_token.access_token
        except SpotifyToken.DoesNotExist:
            return None

    def refresh_access_token(self):
        spotify_token = SpotifyToken.objects.get(user=self.user)

        token_info = self.sp_oauth.refresh_access_token(spotify_token.refresh_token)
        new_access_token = token_info['access_token']
        expires_at = timezone.now() + timezone.timedelta(seconds=token_info['expires_in'])

        spotify_token.access_token = new_access_token
        spotify_token.expires_at = expires_at
        spotify_token.save()

        return new_access_token
