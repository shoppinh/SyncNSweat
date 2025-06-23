from google import genai
import json
from typing import Dict, Any
from app.core.config import settings
from app.models.preferences import Preferences
from app.models.profile import Profile

class GeminiService:
    def __init__(self):
        """
        Initializes the Gemini Service client using the API key from settings.
        """
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

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
         + Music genres: {user_preferences.music_genres if user_preferences.music_genres else []}
         + Music tempo: {user_preferences.music_tempo if user_preferences.music_tempo else 'medium'}


        Format the response as a valid JSON object with the following keys:
        - "exercises": a list of exercise objects, each with "name", "sets", "reps", "machine" and "rest" in minutes.
        - "intensity": an integer representing the overall workout intensity from 1 to 10.
        - "duration": an integer for the recommended workout duration in minutes.
        - "notes": a string containing any specific form or safety tips.
        - "spotify_playlist": a string with the recommended Spotify playlist ID or name for workout music.
        """
        

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        try:
            # Clean up potential markdown formatting from the response
            cleaned_response = response.text.strip().lstrip('```json').rstrip('```').strip()
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
        try:
            # Clean up potential markdown formatting from the response
            cleaned_response = response.text.strip().lstrip('```json').rstrip('```').strip()
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, AttributeError):
            return {
                "target_tempo": 128,
                "target_energy": 0.8,
                "target_valence": 0.7,
                "target_danceability": 0.7
            }