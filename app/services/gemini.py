from google import genai
import json
from typing import Dict, Any, Optional, List, cast
from app.core.config import settings
from app.models.preferences import Preferences
from app.models.user import User
from app.schemas.preferences import PreferencesResponse
from app.schemas.profile import ProfileResponse
from app.models.profile import Profile
from app.services.spotify import SpotifyService
from app.services.user import UserService
from sqlalchemy.orm import Session

_JSON_BLOCK_START = '```json'
_JSON_BLOCK_END = '```'

class GeminiService:
    def __init__(self, db: Session, current_user: Optional[User] = None):
        """
        Initializes the Gemini Service client using the API key from settings.
        """
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'
        self.spotify_service = SpotifyService(db, current_user=current_user)
        self.user_service = UserService(db)

    async def get_workout_recommendations(self, user_profile: Profile, user_preferences: Preferences, workout_type: str) -> Dict[str, Any]:
        """
        Generate personalized workout recommendations using the Gemini AI model asynchronously.
        """
        prompt = f"""
        As a fitness expert, create a personalized {workout_type} workout plan for:
        - Fitness level: {user_profile.fitness_level if user_profile.fitness_level else 'beginner'}
        - Fitness goal: {user_profile.fitness_goal if user_profile.fitness_goal else 'general_fitness'}
        - Available days: {user_profile.available_days if user_profile.available_days else ['Monday', 'Wednesday', 'Friday']}
        - Workout duration: {user_profile.workout_duration_minutes if user_profile.workout_duration_minutes else 45}
        - Preferences:
         + Available equipment: {user_preferences.available_equipment if user_preferences.available_equipment else ['dumbbells', 'resistance bands']}
         + Target muscle groups: {user_preferences.target_muscle_groups if user_preferences.target_muscle_groups else []}
         + Exercise types: {user_preferences.exercise_types if user_preferences.exercise_types else ['strength', 'cardio']}

        Format the response as a valid JSON object with the following keys:
        - "exercises": a list of exercise objects, each with "name", "sets", "reps", "machine" and "rest" in minutes.
        - "intensity": an integer representing the overall workout intensity from 1 to 10.
        - "duration": an integer for the recommended workout duration in minutes.
        - "notes": a string containing any specific form or safety tips.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        text = getattr(response, 'text', None)
        if not isinstance(text, str):
            return {
                "exercises": [],
                "intensity": 5,
                "duration": 45,
                "notes": "Unable to parse AI response. Please try again.",
                "spotify_playlist": "default-workout-playlist"
            }
        try:
            cleaned_response = text.strip().lstrip(_JSON_BLOCK_START).rstrip(_JSON_BLOCK_END).strip()
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, AttributeError):
            return {
                "exercises": [],
                "intensity": 5,
                "duration": 45,
                "notes": "Unable to parse AI response. Please try again.",
                "spotify_playlist": "default-workout-playlist"
            }

    async def enhance_playlist_parameters(self, workout_type: str, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate enhanced music parameters for workouts using the Gemini AI model asynchronously.
        """
        prompt = f"""
        As a fitness music expert, recommend Spotify API parameters for a {workout_type} workout based on the following user preferences:
        - User's preferred genres: {user_preferences.get('genres', [])}
        - Workout intensity: {user_preferences.get('intensity', 'medium')}
        - Workout duration: {user_preferences.get('duration_minutes', 45)} minutes

        Return only a single, valid JSON object with the following keys for the Spotify API:
        - "target_tempo": a number representing the target BPM.
        - "target_energy": a float between 0.0 and 1.0.
        - "target_valence": a float between 0.0 and 1.0.
        - "target_danceability": a float between 0.0 and 1.0.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        text = getattr(response, 'text', None)
        if not isinstance(text, str):
            return {
                "target_tempo": 128,
                "target_energy": 0.8,
                "target_valence": 0.7,
                "target_danceability": 0.7
            }
        try:
            cleaned_response = text.strip().lstrip(_JSON_BLOCK_START).rstrip(_JSON_BLOCK_END).strip()
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, AttributeError):
            return {
                "target_tempo": 128,
                "target_energy": 0.8,
                "target_valence": 0.7,
                "target_danceability": 0.7
            }

    async def recommend_spotify_playlist(self, user_profile: ProfileResponse, user_preferences: PreferencesResponse, workout_type: str, duration_minutes: int) -> Dict[str, Any]:
        # Fetch user's Spotify data
        try:
            spotify_data: Dict[str, Any] = {}
            if hasattr(user_preferences, 'spotify_data') and user_preferences.spotify_data is not None:
                spotify_data = cast(Dict[str, Any], user_preferences.spotify_data)
            access_token = spotify_data.get('access_token', '')
            refresh_token = spotify_data.get('refresh_token', '')
            top_tracks_raw = await self.spotify_service.get_current_user_top_tracks(access_token)
            top_tracks_items = top_tracks_raw.get('items', []) if isinstance(top_tracks_raw, dict) else []
            top_track_names: List[str] = [str(track.get('name', '')) for track in top_tracks_items if isinstance(track, dict) and 'name' in track]
            top_artists_raw = await self.spotify_service.get_current_user_top_artists(access_token)
            top_artists_items = top_artists_raw.get('items', []) if isinstance(top_artists_raw, dict) else []
            top_artist_names: List[str] = [str(artist.get('name', '')) for artist in top_artists_items if isinstance(artist, dict) and 'name' in artist]
        except Exception:
            return {
                "message": "Error fetching Spotify data. Please ensure your Spotify account is connected and try again.",
                "playlist_recommendations": [],
                "playlist_url": None
            }

        prompt = f"""
        You are a music curator. Your goal is to recommend a Spotify playlist based on the user's preferences.
        Here's the user's information:
        - User ID: {getattr(user_profile, 'id', 'unknown')}
        - Preferred Genres: {', '.join(getattr(user_preferences, 'music_genres', [])) if getattr(user_preferences, 'music_genres', None) else 'None'}
        - User's Top Tracks: {', '.join(top_track_names[:5]) if top_track_names else 'None'}
        - User's Top Artists: {', '.join(top_artist_names[:5]) if top_artist_names else 'None'}

        Please suggest 10-15 songs and artists for a Spotify playlist within the duration of {duration_minutes} minutes. Provide the output in a structured JSON format.
        The JSON should have a 'playlist_recommendations' key, which is a list of dicts.
        Each dict should have:
        - 'song_title': (string)
        - 'artist_name': (string)
        - 'reason': (string) A very brief reason for the recommendation (1-2 sentences).

        Example JSON structure:
        {{
            "playlist_recommendations": [
                {{
                    "song_title": "Blinding Lights",
                    "artist_name": "The Weeknd",
                    "reason": "Upbeat and energetic, perfect for a high-intensity workout."
                }},
                {{
                    "song_title": "Levitating",
                    "artist_name": "Dua Lipa",
                    "reason": "Catchy and motivating, great for keeping the energy high."
                }}
            ]
        }}
        """
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            text = getattr(response, 'text', None)
            if not isinstance(text, str):
                raise ValueError('No response text from Gemini')
            response_text = text.strip().lstrip(_JSON_BLOCK_START).rstrip(_JSON_BLOCK_END).strip()
            playlist_recommendations_json = json.loads(response_text)
            refresh_token = spotify_data.get('refresh_token', '')
            user_spotify_profile = await self.spotify_service.get_user_profile(
                access_token,
                refresh_token,
                self.user_service.update_access_token
            )
            recommended_tracks_uris: List[str] = []
            for rec in playlist_recommendations_json.get('playlist_recommendations', []):
                if not (isinstance(rec, dict) and 'song_title' in rec and 'artist_name' in rec):
                    continue
                search_query = f"track:{rec['song_title']} artist:{rec['artist_name']}"
                search_results = await self.spotify_service.search_tracks(access_token, search_query)
                if search_results and isinstance(search_results, dict):
                    tracks = search_results.get('tracks', {})
                    items = tracks.get('items', []) if isinstance(tracks, dict) else []
                    if items and isinstance(items[0], dict) and 'uri' in items[0]:
                        recommended_tracks_uris.append(items[0]['uri'])
            if recommended_tracks_uris:
                playlist_name = f"SyncNSweat - {', '.join(getattr(user_preferences, 'music_genres', []))} {workout_type} Playlist"
                new_playlist = await self.spotify_service.create_playlist(
                    access_token,
                    refresh_token,
                    user_spotify_profile.get('id', '') if isinstance(user_spotify_profile, dict) else '',
                    playlist_name,
                    public=False
                )
                if new_playlist and isinstance(new_playlist, dict) and 'id' in new_playlist and 'external_urls' in new_playlist and 'spotify' in new_playlist['external_urls']:
                    await self.spotify_service.add_tracks_to_playlist(
                        access_token,
                        new_playlist['id'],
                        recommended_tracks_uris
                    )
                    return {"message": "Playlist created and tracks added!", "playlist_url": new_playlist['external_urls']['spotify']}
                else:
                    return {"message": "Could not create Spotify playlist."}
            else:
                return {"message": "No tracks found for the recommendations."}
        except Exception:
            return {
                "message": "Error processing playlist recommendations. Please try again.",
                "playlist_recommendations": [],
                "playlist_url": None
            }