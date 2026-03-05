# Spotify to Apple Music Playlist Converter

A simple, private, and secure Python script to migrate your Spotify playlists to Apple Music. 

Unlike free online playlist converters that request full access to your accounts and harvest your data, this script runs 100% locally on your machine. Your data remains strictly between you, Spotify, and Apple.

## Features
- **Privacy First:** No third-party tracking, no data harvesting.
- **Secure:** Uses environment variables to protect your API keys.
- **Fault Tolerant:** Automatically skips songs that don't exist in the Apple Music catalog without crashing.

## Prerequisites
- Python 3.7+
- A [Spotify Developer Account](https://developer.spotify.com/) (to get a Client ID and Secret)
- An Apple Developer Account (to generate an Apple Music Developer Token and User Token)

## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/pullclone/](https://github.com/pullclone/playlist-switch.git)
   cd spotify-to-apple-music
   ```
2. Install the required Python dependencies:
   ```bash
   pip install requests
   ```

## Configuration (Environment Variables)
To keep your credentials secure, do not paste them into the code. Set them as environment variables in your terminal before running the script.

**On macOS / Linux:**
```bash
export SPOTIFY_CLIENT_ID="your_spotify_client_id"
export SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
export APPLE_MUSIC_DEVELOPER_TOKEN="your_apple_music_developer_token"
export APPLE_MUSIC_USER_TOKEN="your_apple_music_user_token"
```

**On Windows (Command Prompt):**
```cmd
set SPOTIFY_CLIENT_ID="your_spotify_client_id"
set SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
set APPLE_MUSIC_DEVELOPER_TOKEN="your_apple_music_developer_token"
set APPLE_MUSIC_USER_TOKEN="your_apple_music_user_token"
```

## Usage
1. Open `converter.py` in a text editor.
2. Update the `SPOTIFY_PLAYLIST_ID` variable with the ID of the playlist you want to convert. 
3. *(Optional)* Update the `APPLE_MUSIC_PLAYLIST_NAME` variable.
4. Run the script:
   ```bash
   python converter.py
   ```

## Disclaimer
This script is provided as-is. It is not affiliated with or endorsed by Spotify or Apple.
