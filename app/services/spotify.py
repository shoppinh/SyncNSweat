import base64
import requests
from typing import Dict, List, Optional, Any
from app.core.config import settings
from app.services.gemini import GeminiService  # Import GeminiService

class SpotifyService:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
        self.gemini_service = GeminiService()  # Initialize GeminiService
    
    def get_auth_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """
        Get the Spotify authorization URL.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
        }
        if state:
            params["state"] = state
        
        auth_url = f"{self.auth_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
        return auth_url
    
    def get_access_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        """
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        return response.json()
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an access token.
        """
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        return response.json()
    
    def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get the user's Spotify profile.
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(f"{self.api_base_url}/me", headers=headers)
        return response.json()
    
    def get_user_playlists(self, access_token: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get the user's playlists.
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(f"{self.api_base_url}/me/playlists?limit={limit}", headers=headers)
        return response.json()
    
    def create_playlist(
        self,
        access_token: str,
        user_id: str,
        name: str,
        description: str = "",
        public: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new playlist.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "description": description,
            "public": public
        }
        
        response = requests.post(
            f"{self.api_base_url}/users/{user_id}/playlists",
            headers=headers,
            json=data
        )
        return response.json()
    
    def add_tracks_to_playlist(
        self,
        access_token: str,
        playlist_id: str,
        track_uris: List[str]
    ) -> Dict[str, Any]:
        """
        Add tracks to a playlist.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "uris": track_uris
        }
        
        response = requests.post(
            f"{self.api_base_url}/playlists/{playlist_id}/tracks",
            headers=headers,
            json=data
        )
        return response.json()
    
    def get_seed_tracks(self, access_token: str, genres: list, workout_type: str) -> list:
        """Get seed tracks based on genres and workout type."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Map workout types to appropriate genres
        workout_genres = {
            "cardio": ["electronic", "dance", "pop"],
            "strength": ["hip-hop", "rock", "metal"],
            "yoga": ["ambient", "chill", "classical"],
        }

        # Combine workout-specific genres with user preferences
        selected_genres = workout_genres.get(workout_type, [])
        if genres:
            selected_genres.extend([g for g in genres if g not in selected_genres])
        selected_genres = selected_genres[:5]  # Spotify allows max 5 seed genres

        # Get recommendations based on genres to use as seeds
        params = {
            "seed_genres": ",".join(selected_genres[:5]),
            "limit": 2  # Get 2 tracks to use as seeds
        }
        
        response = requests.get(
            f"{self.api_base_url}/recommendations",
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get seed tracks: {response.json()}")
            
        tracks = response.json().get("tracks", [])
        return [track["id"] for track in tracks]

    async def calculate_target_parameters(self, workout_type: str, music_tempo: str, user_preferences: dict) -> dict:
        """Enhanced target parameters using Gemini AI."""
        # Get AI-enhanced parameters
        enhanced_params = await self.gemini_service.enhance_playlist_parameters(
            workout_type,
            user_preferences
        )
        
        # Merge with existing parameters
        base_params = super().calculate_target_parameters(workout_type, music_tempo)
        return {**base_params, **enhanced_params}

    def get_recommendations(self, access_token: str, seed_tracks: list, 
                          target_params: dict, duration_minutes: int) -> dict:
        """Get track recommendations from Spotify."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Calculate number of tracks needed based on duration
        avg_track_duration = 3.5 * 60 * 1000  # 3.5 minutes in milliseconds
        target_track_count = int((duration_minutes * 60 * 1000) / avg_track_duration)
        
        # Prepare parameters for recommendations API
        params = {
            "limit": min(target_track_count + 5, 100),  # Add buffer, max 100
            "seed_tracks": ",".join(seed_tracks),
            "min_popularity": 20,  # Ensure somewhat popular tracks
        }
        
        # Add target parameters
        params.update({
            f"target_{key}": value 
            for key, value in target_params.items()
        })
        
        response = requests.get(
            f"{self.api_base_url}/recommendations",
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get recommendations: {response.json()}")
        
        return response.json()

    def create_workout_playlist(self, access_token: str, track_uris: list, 
                              workout_type: str, user_id: str) -> dict:
        """Create a new playlist with the recommended tracks."""
        # Get user profile for display name
        user_profile = self.get_user_profile(access_token)
        display_name = user_profile.get("display_name", "User")
        
        # Create playlist name and description
        workout_names = {
            "cardio": "Cardio Boost",
            "strength": "Power Mix",
            "yoga": "Zen Flow",
        }
        playlist_name = f"{workout_names.get(workout_type, 'Workout')} for {display_name}"
        description = f"Custom {workout_type.title()} workout playlist created by SyncNSweat"
        
        # Create the playlist
        playlist = self.create_playlist(
            access_token=access_token,
            user_id=user_id,
            name=playlist_name,
            description=description,
            public=False  # Keep private by default
        )
        
        if "id" not in playlist:
            raise Exception(f"Failed to create playlist: {playlist}")
        
        # Add tracks to the playlist
        result = self.add_tracks_to_playlist(
            access_token=access_token,
            playlist_id=playlist["id"],
            track_uris=track_uris
        )
        
        if "snapshot_id" not in result:
            raise Exception(f"Failed to add tracks to playlist: {result}")
        
        # Return playlist details
        return {
            "id": playlist["id"],
            "name": playlist_name,
            "external_url": playlist["external_urls"]["spotify"],
            "image_url": playlist["images"][0]["url"] if playlist.get("images") else None,
        }



