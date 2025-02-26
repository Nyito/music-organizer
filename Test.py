import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

client_id = os.getenv('ClientID')
client_secret = os.getenv('Clientsecret')
redirect_url = os.getenv('RedirectURL')

scope = 'user-read-private user-read-email user-library-read user-read-recently-played user-top-read'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

auth_url = sp.auth_manager.get_authorize_url()
print(auth_url)

conn = sqlite3.connect("spotify_data.db")
cursor = conn.cursor()

user = sp.current_user()
cursor.execute("INSERT OR IGNORE INTO users (id, display_name, country) VALUES (?, ?, ?)",
               (user['id'], user['display_name'], user['country']))
conn.commit()

# top_artists = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')  # Can use 'short_term' or 'medium_term'
# for idx, artist in enumerate(top_artists['items']):
#     print(f"{idx+1}. {artist['name']} - {artist['genres']}")

top_tracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
for idx, track in enumerate(top_tracks['items']):
    track_id = track['id']
    cursor.execute("INSERT OR IGNORE INTO tracks (id, name, artist, album, popularity, duration_ms) VALUES (?, ?, ?, ?, ?, ?)",
                   (track_id, track['name'], track['artists'][0]['name'], track['album']['name'], track['popularity'], track['duration_ms']))
    print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")

conn.commit()
conn.close()
print("Data stored succesfully!")

# recent_tracks = sp.current_user_recently_played(limit=50)
# for idx, track in enumerate(recent_tracks['items']):
#     print(f"{idx+1}. {track['track']['name']} - {track['track']['artists'][0]['name']} at {track['played_at']}")