from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, cast

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences
from app.models.workout import Workout
from app.services.gemini import GeminiService
from app.services.spotify import SpotifyService
from app.services.playlist_selector import PlaylistSelectorService
from app.core.security import get_current_user
from app.dependencies.spotify import get_spotify_service, get_token_manager, get_user_repository
from app.services.spotify_token_manager import SpotifyTokenManager
from app.repositories.user_repository import UserRepository
from app.utils.constants import (
    SPOTIFY_NOT_CONNECTED,
    SPOTIFY_REFRESH_TOKEN_NOT_FOUND,
    SPOTIFY_ACCESS_TOKEN_NOT_FOUND,
    USER_PROFILE_NOT_FOUND,
    WORKOUT_NOT_FOUND,
    PROFILE_NOT_FOUND,
    PREFERENCES_NOT_FOUND,
    USING_EXISTING_PLAYLIST,
    SELECTED_NEW_PLAYLIST
)

router = APIRouter()


@router.get("/spotify/auth-url")
def get_spotify_auth_url(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    token_manager: SpotifyTokenManager = Depends(get_token_manager)
):
    """
    Get Spotify authorization URL.
    """
    spotify_service = SpotifyService(token_manager)
    redirect_uri = f"{settings.SPOTIFY_REDIRECT_URL}/api/v1/auth/spotify/callback"
    auth_url = spotify_service.get_auth_url(redirect_uri, state=str(current_user.id))

    return {"auth_url": auth_url}


@router.get("/spotify/recommendations")
async def get_spotify_recommendations(
    workout_type: str = "",
    duration_minutes: int = 60,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
    spotify_service: SpotifyService = Depends(get_spotify_service),
):
    """
    Get Spotify playlist recommendations based on user preferences and workout type.
    """
    current_user_id = cast(int, current_user.id)
    # Check if Spotify is connected using repository
    if not user_repository.is_spotify_connected(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=SPOTIFY_NOT_CONNECTED
        )

    # Get Spotify data from repository
    refresh_token = user_repository.get_spotify_refresh_token(cast(int, current_user.id))
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SPOTIFY_REFRESH_TOKEN_NOT_FOUND,
        )

    # Get user profile and preferences data
    profile = user_repository.get_profile(current_user_id)
    preferences = user_repository.get_preferences(current_user_id)
    
    if not profile or not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND
        )

    # Initialize GeminiService with Spotify service (pure business logic)
    gemini_service = GeminiService(spotify_service)

    # Convert model objects to dictionaries for the service
    profile_data = {
        'id': profile.id,
        'fitness_level': profile.fitness_level,
        'fitness_goal': profile.fitness_goal,
        'available_days': profile.available_days,
        'workout_duration_minutes': profile.workout_duration_minutes,
    }
    
    preferences_data = {
        'music_genres': preferences.music_genres,
        'available_equipment': preferences.available_equipment,
        'target_muscle_groups': preferences.target_muscle_groups,
        'exercise_types': preferences.exercise_types,
    }

    # Get recommendations from Gemini (pure business logic)
    recommendations = await gemini_service.recommend_spotify_playlist(
        user_id=current_user_id,
        refresh_token=refresh_token,
        user_profile=profile_data,
        user_preferences=preferences_data,
        workout_type=workout_type,
        duration_minutes=duration_minutes
    )

    return recommendations


@router.get("/spotify/playlists")
async def get_user_playlists(
    current_user: User = Depends(get_current_user), 
    user_repository: UserRepository = Depends(get_user_repository),
    spotify_service: SpotifyService = Depends(get_spotify_service),
):
    """
    Get user's Spotify playlists.
    """
    current_user_id = cast(int, current_user.id)
    # Check if Spotify is connected using repository
    if not user_repository.is_spotify_connected(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=SPOTIFY_NOT_CONNECTED
        )

    # Get Spotify data from repository
    refresh_token = user_repository.get_spotify_refresh_token(current_user_id)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SPOTIFY_REFRESH_TOKEN_NOT_FOUND,
        )

    # Get user playlists using the new service (pure business logic)
    playlists_data = await spotify_service.get_user_playlists(
        current_user_id, refresh_token
    )

    return playlists_data


@router.get("/workout/{workout_id}")
def get_playlist_for_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a playlist for a specific workout.
    """
    # Get the workout
    workout = (
        db.query(Workout)
        .filter(Workout.id == workout_id, Workout.user_id == current_user.id)
        .first()
    )

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=WORKOUT_NOT_FOUND
        )

    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PROFILE_NOT_FOUND
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PREFERENCES_NOT_FOUND
        )
        
    is_spotify_connected = cast(bool, preferences.spotify_connected)
    # Check if Spotify is connected
    if not is_spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=SPOTIFY_NOT_CONNECTED
        )

    # Check if workout already has a playlist
    if cast(bool, workout.playlist_id) and cast(bool, workout.playlist_name):
        return {
            "playlist_id": workout.playlist_id,
            "playlist_name": workout.playlist_name,
            "external_url": f"https://open.spotify.com/playlist/{workout.playlist_id}",
            "message": USING_EXISTING_PLAYLIST,
        }

    # Get Spotify access token from preferences
    spotify_data = cast(Dict[str, Any], preferences.spotify_data)
    if not spotify_data or "access_token" not in spotify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SPOTIFY_ACCESS_TOKEN_NOT_FOUND,
        )

    access_token = spotify_data["access_token"]

    # Check if token needs to be refreshed
    if "refresh_token" in spotify_data:
        # In a real implementation, we would check if the token is expired
        # and refresh it if needed
        pass

    # Select a playlist for the workout
    playlist_selector = PlaylistSelectorService()
    playlist = playlist_selector.select_playlist_for_workout(
        access_token=access_token,
        workout_focus=cast(str, workout.focus),
        music_genres=cast(List[str], preferences.music_genres),
        music_tempo=cast(str, preferences.music_tempo),
        recently_used_playlists=[],  # In a real implementation, we would track recently used playlists
    )

    # Update the workout with the playlist info
    workout.playlist_id = playlist["id"]
    workout.playlist_name = playlist["name"]
    db.add(workout)
    db.commit()

    return {
        "playlist_id": playlist["id"],
        "playlist_name": playlist["name"],
        "external_url": playlist["external_url"],
        "image_url": playlist["image_url"],
        "message": SELECTED_NEW_PLAYLIST,
    }


@router.get("/workout/{workout_id}/refresh")
def refresh_playlist_for_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a new playlist for a workout.
    """
    # Get the workout
    workout = (
        db.query(Workout)
        .filter(Workout.id == workout_id, Workout.user_id == current_user.id)
        .first()
    )

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=WORKOUT_NOT_FOUND
        )

    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PROFILE_NOT_FOUND
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PREFERENCES_NOT_FOUND
        )

    # Check if Spotify is connected
    is_spotify_connected = cast(bool, preferences.spotify_connected)
    if not is_spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=SPOTIFY_NOT_CONNECTED
        )

    # Get Spotify access token from preferences
    spotify_data = cast(Dict[str, Any], preferences.spotify_data)
    if not spotify_data or "access_token" not in spotify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SPOTIFY_ACCESS_TOKEN_NOT_FOUND,
        )

    access_token = spotify_data["access_token"]

    # Check if token needs to be refreshed
    if "refresh_token" in spotify_data:
        # In a real implementation, we would check if the token is expired
        # and refresh it if needed
        pass

    # Get the current playlist ID to avoid selecting it again
    recently_used_playlists = []
    if cast(bool, workout.playlist_id):
        recently_used_playlists.append(cast(str, workout.playlist_id))

    # Select a new playlist for the workout
    playlist_selector = PlaylistSelectorService()
    playlist = playlist_selector.select_playlist_for_workout(
        access_token=access_token,
        workout_focus=cast(str, workout.focus),
        music_genres=cast(List[str], preferences.music_genres),
        music_tempo=cast(str, preferences.music_tempo),
        recently_used_playlists=recently_used_playlists,
    )

    # Update the workout with the new playlist info
    workout.playlist_id = playlist["id"]
    workout.playlist_name = playlist["name"]
    db.add(workout)
    db.commit()

    return {
        "playlist_id": playlist["id"],
        "playlist_name": playlist["name"],
        "external_url": playlist["external_url"],
        "image_url": playlist["image_url"],
        "message": SELECTED_NEW_PLAYLIST,
    }
