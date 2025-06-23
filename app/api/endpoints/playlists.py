from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences
from app.models.workout import Workout
from app.services.spotify import SpotifyService
from app.services.playlist_selector import PlaylistSelectorService
from app.core.security import get_current_user

router = APIRouter()


@router.get("/spotify/auth-url")
def get_spotify_auth_url(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get Spotify authorization URL.
    """
    spotify_service = SpotifyService()
    redirect_uri = f"{settings.SPOTIFY_REDIRECT_URL}/api/v1/auth/spotify/callback"
    auth_url = spotify_service.get_auth_url(redirect_uri, state=str(current_user.id))

    return {"auth_url": auth_url}


@router.get("/spotify/recommendations")
def get_spotify_recommendations(
    workout_type: str = None,
    duration_minutes: int = 60,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get Spotify playlist recommendations based on user preferences and workout type.
    """
    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify not connected"
        )

    # Get Spotify access token from preferences
    spotify_data = preferences.spotify_data
    if not spotify_data or "access_token" not in spotify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify access token not found",
        )

    access_token = spotify_data["access_token"]

    # Initialize SpotifyService
    spotify_service = SpotifyService()
    playlist_selector = PlaylistSelectorService()

    # Get seed tracks and genres based on preferences and workout type
    seed_tracks = spotify_service.get_seed_tracks(
        access_token=access_token,
        genres=preferences.music_genres,
        workout_type=workout_type,
    )

    # # Calculate target parameters based on workout type and preferences
    target_params = playlist_selector.calculate_target_params(
        workout_focus=workout_type, music_tempo=preferences.music_tempo
    )

    # Get recommendations from Spotify
    recommendations = spotify_service.get_recommendations(
        access_token=access_token,
        seed_tracks=seed_tracks,
        target_tempo=target_params["target_tempo"],
        target_energy=target_params["target_energy"],
    )

    # Create a new playlist for the workout
    playlist = spotify_service.create_workout_playlist(
        access_token=access_token,
        track_uris=[track["uri"] for track in recommendations["tracks"]],
        workout_type=workout_type,
        user_id=current_user.id,
    )

    return {
        "playlist_id": playlist["id"],
        "playlist_name": playlist["name"],
        "tracks": [
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "duration_ms": track["duration_ms"],
                "uri": track["uri"],
            }
            for track in recommendations["tracks"]
        ],
        "total_duration_minutes": duration_minutes,
        "external_url": playlist["external_url"],
        "image_url": playlist.get("image_url"),
    }


@router.get("/spotify/playlists")
def get_user_playlists(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get user's Spotify playlists.
    """
    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify not connected"
        )

    # This is a placeholder for the actual Spotify playlists logic
    # In a real implementation, we would use the SpotifyService to get the user's playlists

    # Mock response
    return {
        "playlists": [
            {"id": "playlist1", "name": "Workout Mix 1", "tracks": 15},
            {"id": "playlist2", "name": "Cardio Playlist", "tracks": 20},
            {"id": "playlist3", "name": "Strength Training", "tracks": 18},
        ]
    }


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
            status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found"
        )

    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify not connected"
        )

    # Check if workout already has a playlist
    if workout.playlist_id and workout.playlist_name:
        return {
            "playlist_id": workout.playlist_id,
            "playlist_name": workout.playlist_name,
            "external_url": f"https://open.spotify.com/playlist/{workout.playlist_id}",
            "message": "Using existing playlist",
        }

    # Get Spotify access token from preferences
    spotify_data = preferences.spotify_data
    if not spotify_data or "access_token" not in spotify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify access token not found",
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
        workout_focus=workout.focus,
        music_genres=preferences.music_genres,
        music_tempo=preferences.music_tempo,
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
        "message": "Selected new playlist for workout",
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
            status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found"
        )

    # Get user profile and preferences
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    # Check if Spotify is connected
    if not preferences.spotify_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify not connected"
        )

    # Get Spotify access token from preferences
    spotify_data = preferences.spotify_data
    if not spotify_data or "access_token" not in spotify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify access token not found",
        )

    access_token = spotify_data["access_token"]

    # Check if token needs to be refreshed
    if "refresh_token" in spotify_data:
        # In a real implementation, we would check if the token is expired
        # and refresh it if needed
        pass

    # Get the current playlist ID to avoid selecting it again
    recently_used_playlists = []
    if workout.playlist_id:
        recently_used_playlists.append(workout.playlist_id)

    # Select a new playlist for the workout
    playlist_selector = PlaylistSelectorService()
    playlist = playlist_selector.select_playlist_for_workout(
        access_token=access_token,
        workout_focus=workout.focus,
        music_genres=preferences.music_genres,
        music_tempo=preferences.music_tempo,
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
        "message": "Selected new playlist for workout",
    }
