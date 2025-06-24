import base64
import requests
from typing import Dict, List, Optional, Any
from app.core.config import settings
from sqlalchemy.orm import Session

from app.models.preferences import Preferences
from app.models.user import User

class SpotifyService:
    def __init__(self, db:Session, current_user: Optional[User] = None):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
        self.db = db
        self.current_user = current_user
    
    def get_auth_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """
        Get the Spotify authorization URL.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "user-read-private user-read-email user-library-read user-library-modify user-top-read user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-public playlist-modify-private"
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
    
    async def get_user_profile(
        self,
        access_token: str,
        refresh_token: str,
    ) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.api_base_url}/me"
        response = self._make_request_with_refresh(
            "GET", url, headers, refresh_token
        )
        return response.json()


    async def get_user_playlists(self, access_token: str, refresh_token: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get the user's playlists.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.api_base_url}/me/playlists?limit={limit}"
        response = self._make_request_with_refresh(
            "GET", url, headers, refresh_token
        )
        return response.json()
    
    async def create_playlist(
        self,
        access_token: str,
        refresh_token: str,
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
        
        response = self._make_request_with_refresh(
            "POST",
            f"{self.api_base_url}/users/{user_id}/playlists",
            headers,
            refresh_token=refresh_token,
            data=data,
        )
        return response.json()
    
    async def add_tracks_to_playlist(
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
    
    async def get_seed_tracks(self, access_token: str, genres: list, workout_type: str) -> list:
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

    async def get_current_user_top_tracks(self, access_token: str) -> dict:
        """Get the user's top tracks."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try: 
            response = requests.get(f"{self.api_base_url}/me/top/tracks", headers=headers)
            return {
                "items": response.json().get("items", [])
            }
        except Exception as e:
            return {
                "items": []
            }
        
    
    
    async def get_current_user_top_artists(self, access_token: str) -> dict:
        """Get the user's top artists."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = requests.get(f"{self.api_base_url}/me/top/artists", headers=headers)
            return {
                "items": response.json().get("items", [])
            }
        except Exception as e:
            return {
                "items": []
            }
        
    async def search_tracks(self, access_token: str, search_query: str) -> dict:
        """Search for tracks."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{self.api_base_url}/search", headers=headers, params={"q": search_query, "type": "track"})
        return response.json()
    
    def _default_update_access_token(self, new_access_token: str, user: Optional[User], db: Session):
        """
        Fallback function to update the user's access token in the database if no callback is provided.
        """
        if user is not None:
            preferences = db.query(Preferences).filter(Preferences.user_id == user.id).first()
            if preferences is not None:
                preferences.spotifyData.access_token = new_access_token
                db.add(preferences)
                db.commit()

    def _make_request_with_refresh(
        self,
        method: str,
        url: str,
        headers: dict,
        refresh_token: str,
        update_access_token_callback=None,
        **kwargs
    ):
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 401 and refresh_token:
            # Token expired, refresh it
            token_data = self.refresh_access_token(refresh_token)
            new_access_token = token_data.get("access_token")
            if not new_access_token:
                raise Exception("Failed to refresh access token")
            # Update the access token wherever you store it (session/db)
            if update_access_token_callback is not None:
                update_access_token_callback(new_access_token, self.current_user)
            else:
                self._default_update_access_token(new_access_token, self.current_user, self.db)
            headers["Authorization"] = f"Bearer {new_access_token}"
            # Retry the request
            response = requests.request(method, url, headers=headers, **kwargs)
        return response




