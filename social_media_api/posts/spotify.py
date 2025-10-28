# posts/spotify.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def get_track_info(track_id):
    sp = get_spotify_client()
    track = sp.track(track_id)
    return {
        "song_title": track['name'],
        "artist": ", ".join([artist['name'] for artist in track['artists']]),
        "album_cover_url": track['album']['images'][0]['url'] if track['album']['images'] else None
    }
