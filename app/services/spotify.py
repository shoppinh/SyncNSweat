import base64
import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
import httpx
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.spotify_token_manager import SpotifyTokenManager


class SpotifyService:
    def __init__(self, token_manager: SpotifyTokenManager):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
        self.token_manager = token_manager
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=settings.SPOTIFY_REQUEST_TIMEOUT)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    def get_auth_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """Get the Spotify authorization URL."""
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
    
    async def get_access_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
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
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
    
    async def _refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token with retry logic"""
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        
        for attempt in range(settings.SPOTIFY_MAX_RETRIES):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.token_url, headers=headers, data=data
                    )
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                if attempt == settings.SPOTIFY_MAX_RETRIES - 1:
                    raise ValueError(f"Token refresh failed after {settings.SPOTIFY_MAX_RETRIES} attempts: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        # This should never be reached due to the exception above, but satisfies type checker
        raise ValueError("Token refresh failed")
    
    async def _get_valid_token(self, user_id: int, refresh_token: str, 
                              update_callback: Optional[Callable] = None) -> str:
        """Get valid access token, refreshing if necessary"""
        cached_token = self.token_manager.get_cached_token(user_id)
        
        if cached_token and not self.token_manager.is_token_expired(cached_token):
            return cached_token['access_token']
        
        # Refresh token
        token_data = await self._refresh_token(refresh_token)
        if not token_data.get('access_token'):
            raise ValueError("Failed to refresh access token")
        
        # Update database via callback
        if update_callback:
            await update_callback(token_data['access_token'], user_id)
        
        # Cache new token
        expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
        token_data['expires_at'] = expires_at.isoformat()
        self.token_manager.cache_token(user_id, token_data, token_data['expires_in'])
        
        return token_data['access_token']
    
    async def _make_authenticated_request(
        self, 
        method: str, 
        endpoint: str, 
        user_id: int, 
        refresh_token: str,
        update_callback: Optional[Callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated request with automatic token refresh"""
        access_token = await self._get_valid_token(user_id, refresh_token, update_callback)
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {access_token}'
        kwargs['headers'] = headers
        
        url = f"{self.api_base_url}{endpoint}"
        
        for attempt in range(settings.SPOTIFY_MAX_RETRIES):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(method, url, **kwargs)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                if attempt == settings.SPOTIFY_MAX_RETRIES - 1:
                    raise ValueError(f"Request failed after {settings.SPOTIFY_MAX_RETRIES} attempts: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        # This should never be reached due to the exception above, but satisfies type checker
        raise ValueError("Request failed")
    
    # Public methods using the token manager
    async def get_user_profile(self, user_id: int, refresh_token: str
                              ) -> Dict[str, Any]:
        """Get user profile with automatic token management"""
        return await self._make_authenticated_request(
            "GET", "/me", user_id, refresh_token
        )
    
    async def get_user_playlists(self, user_id: int, refresh_token: str, 
                                limit: int = 50) -> Dict[str, Any]:
        """Get user playlists with automatic token management"""
        return await self._make_authenticated_request(
            "GET", f"/me/playlists?limit={limit}", user_id, refresh_token
        )
    
    async def create_playlist(
        self,
        user_id: int,
        refresh_token: str,
        spotify_user_id: str,
        name: str,
        description: str = "",
        public: bool = False
    ) -> Dict[str, Any]:
        """Create a new playlist with automatic token management"""
        data = {
            "name": name,
            "description": description,
            "public": public
        }
        
        return await self._make_authenticated_request(
            "POST",
            f"/users/{spotify_user_id}/playlists",
            user_id,
            refresh_token,
            json=data,
        )
    
    async def add_tracks_to_playlist(
        self,
        user_id: int,
        refresh_token: str,
        playlist_id: str,
        track_uris: List[str]
    ) -> Dict[str, Any]:
        """Add tracks to a playlist with automatic token management"""
        data = {"uris": track_uris}
        
        return await self._make_authenticated_request(
            "POST",
            f"/playlists/{playlist_id}/tracks",
            user_id,
            refresh_token,
            json=data,
        )
    
    async def get_seed_tracks(self, user_id: int, refresh_token: str, 
                              genres: list, workout_type: str) -> list:
        """Get seed tracks based on genres and workout type with automatic token management"""
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
        
        response = await self._make_authenticated_request(
            "GET",
            "/recommendations",
            user_id,
            refresh_token,
            params=params
        )
        
        tracks = response.get("tracks", [])
        return [track["id"] for track in tracks]

    async def get_current_user_top_tracks(self, user_id: int, refresh_token: str
                                         ) -> dict:
        """Get the user's top tracks with automatic token management"""
        try:
            response = await self._make_authenticated_request(
                "GET", "/me/top/tracks", user_id, refresh_token
            )
            return {"items": response.get("items", [])}
        except Exception as e:
            return {"items": []}
    
    async def get_current_user_top_artists(self, user_id: int, refresh_token: str
                                          ) -> dict:
        """Get the user's top artists with automatic token management"""
        try:
            response = await self._make_authenticated_request(
                "GET", "/me/top/artists", user_id, refresh_token
            )
            return {"items": response.get("items", [])}
        except Exception as e:
            return {"items": []}
        
    async def search_tracks(self, user_id: int, refresh_token: str, 
                           search_query: str) -> dict:
        """Search for tracks with automatic token management"""
        return await self._make_authenticated_request(
            "GET", "/search", user_id, refresh_token,
            params={"q": search_query, "type": "track"}
        )
    
    async def create_workout_playlist(self, user_id: int, refresh_token: str, 
                                     track_uris: list, 
                                     workout_type: str, spotify_user_id: str) -> dict:
        """Create a new playlist with the recommended tracks with automatic token management"""
        # Create playlist name and description
        workout_names = {
            "cardio": "Cardio Boost",
            "strength": "Power Mix",
            "yoga": "Zen Flow",
        }
        playlist_name = f"{workout_names.get(workout_type, 'Workout')} Playlist"
        description = f"Custom {workout_type.title()} workout playlist created by SyncNSweat"
        
        # Create the playlist
        playlist = await self.create_playlist(
            user_id=user_id,
            refresh_token=refresh_token,
            spotify_user_id=spotify_user_id,
            name=playlist_name,
            description=description,
            public=False  # Keep private by default
        )
        
        if "id" not in playlist:
            raise Exception(f"Failed to create playlist: {playlist}")
        
        # Add tracks to the playlist
        result = await self.add_tracks_to_playlist(
            user_id=user_id,
            refresh_token=refresh_token,
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




