from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from connectors.spotify_connector import SpotifyConnector
from django.shortcuts import redirect, render
from django.http import HttpResponse
from authentication.models.spotify_token import SpotifyToken
from django.utils import timezone
from connectors.spotify_connector import SpotifyConnector
import spotipy


class SpotifyViewSet(viewsets.ViewSet):
    permission_classes = []

    def get_access_token(self, user):
        try:
            spotify_token = SpotifyToken.objects.get(user=user)
            if spotify_token.is_token_expired():
                spotify_connector = SpotifyConnector(scope="user-library-read playlist-read-private", user=user)
                spotify_token.access_token = spotify_connector.refresh_access_token()
                spotify_token.save()
            return spotify_token.access_token
        except SpotifyToken.DoesNotExist:
            return None

    @action(detail=False, methods=['get'])
    def login(self, request):
        """
        Redirects the user to Spotify's login page for authentication.
        """
        scope = "user-library-read playlist-read-private"
        spotify_connector = SpotifyConnector(scope=scope, user=request.user)
        auth_url = spotify_connector.get_auth_url()
        return redirect(auth_url)

    @action(detail=False, methods=['get'])
    def callback(self, request):
        """
        Handles the callback from Spotify, exchanges the authorization code for an access token.
        """
        code = request.GET.get('code')
        if not code:
            return HttpResponse("Error: No code provided.", status=400)

        spotify_connector = SpotifyConnector(scope="user-library-read playlist-read-private", user=request.user)
        
        try:
            access_token, refresh_token, expiry_datetime = spotify_connector.handle_callback(code)
            spotify_connector.save_tokens(access_token, refresh_token, expiry_datetime)
            return redirect('dashboard')
        except Exception as e:
            return HttpResponse(f"Error during callback: {str(e)}", status=400)

    @action(detail=False, methods=['get'])
    def playlists(self, request):
        """
        Retrieve the authenticated user's Spotify playlists.
        """
        access_token = self.get_access_token(request.user)
        if not access_token:
            return Response({"error": "User is not authenticated with Spotify."}, status=401)

        # Use the access token to call Spotify API
        sp = spotipy.Spotify(auth=access_token)
        playlists = sp.current_user_playlists()
        
        # Serialize the playlists data
        playlist_data = [{"name": playlist["name"], "tracks": playlist["tracks"]} for playlist in playlists["items"]]
        return Response(playlist_data)

    @action(detail=False, methods=['get'])
    def user_data(self, request):
        """
        Retrieve the authenticated user's Spotify profile data.
        """
        access_token = self.get_access_token(request.user)
        if not access_token:
            return Response({"error": "User is not authenticated with Spotify."}, status=401)

        # Use the access token to call Spotify API
        sp = spotipy.Spotify(auth=access_token)
        user_data = sp.current_user()

        return Response(user_data)