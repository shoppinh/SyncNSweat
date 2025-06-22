import base64
import requests
from typing import Dict, List, Optional, Any
from app.core.config import settings

class SpotifyService:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
    
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
    
    def get_recommendations(
        self,
        access_token: str,
        seed_genres: List[str] = None,
        seed_artists: List[str] = None,
        seed_tracks: List[str] = None,
        limit: int = 20,
        target_energy: float = None,
        target_tempo: float = None
    ) -> Dict[str, Any]:
        """
        Get track recommendations.
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        params = {"limit": limit}
        
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres)
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists)
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks)
        if target_energy is not None:
            params["target_energy"] = target_energy
        if target_tempo is not None:
            params["target_tempo"] = target_tempo
        
        response = requests.get(
            f"{self.api_base_url}/recommendations",
            headers=headers,
            params=params
        )
        return response.json()
