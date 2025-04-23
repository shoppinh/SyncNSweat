from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences
from app.services.spotify import SpotifyService
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/spotify/auth-url")
def get_spotify_auth_url(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get Spotify authorization URL.
    """
    spotify_service = SpotifyService()
    redirect_uri = "http://localhost:8000/api/v1/auth/spotify/callback"
    auth_url = spotify_service.get_auth_url(redirect_uri, state=str(current_user.id))
    
    return {"auth_url": auth_url}

@router.get("/spotify/recommendations")
def get_spotify_recommendations(
    workout_type: str = None,
    duration_minutes: int = 60,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get Spotify playlist recommendations based on user preferences and workout type.
    """
    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    preferences = db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    
    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify not connected"
        )
    
    # This is a placeholder for the actual Spotify recommendation logic
    # In a real implementation, we would:
    # 1. Use the SpotifyService to get recommendations based on preferences
    # 2. Create a playlist for the workout
    # 3. Return the playlist details
    
    # Mock response
    return {
        "playlist_id": "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP",
        "playlist_name": f"Workout Mix: {workout_type or 'General'}",
        "tracks": [
            {"name": "Track 1", "artist": "Artist 1", "duration_ms": 180000},
            {"name": "Track 2", "artist": "Artist 2", "duration_ms": 210000},
            {"name": "Track 3", "artist": "Artist 3", "duration_ms": 195000}
        ],
        "total_duration_minutes": duration_minutes
    }

@router.get("/spotify/playlists")
def get_user_playlists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's Spotify playlists.
    """
    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    preferences = db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    
    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify not connected"
        )
    
    # This is a placeholder for the actual Spotify playlists logic
    # In a real implementation, we would use the SpotifyService to get the user's playlists
    
    # Mock response
    return {
        "playlists": [
            {"id": "playlist1", "name": "Workout Mix 1", "tracks": 15},
            {"id": "playlist2", "name": "Cardio Playlist", "tracks": 20},
            {"id": "playlist3", "name": "Strength Training", "tracks": 18}
        ]
    }
