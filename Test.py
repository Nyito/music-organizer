import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('ClientID')
client_secret = os.getenv('Clientsecret')
redirect_url = os.getenv('RedirectURL')

scope = 'user-read-private user-read-email user-library-read user-read-recently-played user-top-read'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

auth_url = sp.auth_manager.get_authorize_url()
print(auth_url)

top_artists = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')  # Can use 'short_term' or 'medium_term'
for idx, artist in enumerate(top_artists['items']):
    print(f"{idx+1}. {artist['name']} - {artist['genres']}")

top_tracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
for idx, track in enumerate(top_tracks['items']):
    print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")

recent_tracks = sp.current_user_recently_played(limit=50)
for idx, track in enumerate(recent_tracks['items']):
    print(f"{idx+1}. {track['track']['name']} - {track['track']['artists'][0]['name']} at {track['played_at']}")