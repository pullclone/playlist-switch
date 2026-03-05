import os
import requests
import json
import sys

# 1. Securely load credentials from environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
APPLE_MUSIC_DEVELOPER_TOKEN = os.environ.get('APPLE_MUSIC_DEVELOPER_TOKEN')
APPLE_MUSIC_USER_TOKEN = os.environ.get('APPLE_MUSIC_USER_TOKEN')

# Ensure all credentials are set before running
if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, APPLE_MUSIC_DEVELOPER_TOKEN, APPLE_MUSIC_USER_TOKEN]):
    print("Error: Missing API credentials.")
    print("Please ensure SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, APPLE_MUSIC_DEVELOPER_TOKEN, and APPLE_MUSIC_USER_TOKEN are set as environment variables.")
    sys.exit(1)

# 2. Configuration (Change these to match your needs)
SPOTIFY_PLAYLIST_ID = 'your_spotify_playlist_id'
SPOTIFY_PLAYLIST_URL = f'https://api.spotify.com/v1/playlists/{SPOTIFY_PLAYLIST_ID}/tracks'
APPLE_MUSIC_PLAYLIST_NAME = 'Converted from Spotify'

def main():
    print("Authenticating with Spotify...")
    # Authenticate with the Spotify API
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })
    
    if auth_response.status_code != 200:
        print(f"Failed to authenticate with Spotify: {auth_response.text}")
        sys.exit(1)
        
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    print("Fetching Spotify playlist...")
    # Get the list of tracks from the Spotify playlist
    spotify_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(SPOTIFY_PLAYLIST_URL, headers=spotify_headers)
    response_data = response.json()

    if 'items' not in response_data:
        print("Error: Could not retrieve tracks. Check your Spotify Playlist ID.")
        sys.exit(1)

    print("Searching for tracks on Apple Music...")
    apple_music_track_ids =[]
    
    # Common headers for Apple Music API
    apple_headers = {
        'Authorization': f'Bearer {APPLE_MUSIC_DEVELOPER_TOKEN}',
        'Music-User-Token': APPLE_MUSIC_USER_TOKEN,
    }

    # Get the Apple Music ID for each track
    for item in response_data['items']:
        track = item.get('track')
        if not track:
            continue
            
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        
        query_params = {
            'term': f'{track_name} {artist_name}',
            'types': 'songs',
            'limit': '1',
        }
        
        am_response = requests.get('https://api.music.apple.com/v1/catalog/us/search', headers=apple_headers, params=query_params)
        am_response_data = am_response.json()
        
        # Safely extract data to prevent KeyErrors if the song isn't found
        songs_data = am_response_data.get('results', {}).get('songs', {}).get('data',[])
        
        if songs_data:
            apple_music_track_ids.append(songs_data[0]['id'])
            print(f" [Found] {track_name} by {artist_name}")
        else:
            print(f"[Not Found] {track_name} by {artist_name} - Skipping...")

    if not apple_music_track_ids:
        print("No tracks were found on Apple Music. Exiting.")
        sys.exit(1)

    print(f"\nCreating Apple Music playlist: '{APPLE_MUSIC_PLAYLIST_NAME}'...")
    # Create a new Apple Music playlist and add the tracks to it
    apple_headers['Content-Type'] = 'application/json'
    
    playlist_data = {
        'attributes': {
            'name': APPLE_MUSIC_PLAYLIST_NAME,
            'description': 'Converted from Spotify using a local Python script.',
        },
        'relationships': {
            'tracks': {
                'data':[{'id': track_id, 'type': 'songs'} for track_id in apple_music_track_ids]
            }
        },
        'type': 'playlists',
    }
    
    creation_response = requests.post('https://api.music.apple.com/v1/me/library/playlists', headers=apple_headers, data=json.dumps(playlist_data))
    
    if creation_response.status_code in (200, 201):
        print("Success! Playlist created.")
    else:
        print(f"Failed to create playlist. Error: {creation_response.text}")

if __name__ == "__main__":
    main()
