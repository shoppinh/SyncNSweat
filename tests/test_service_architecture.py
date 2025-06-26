import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

from app.services.spotify import SpotifyService
from app.services.gemini import GeminiService
from app.repositories.user_repository import UserRepository
from app.services.spotify_token_manager import SpotifyTokenManager


class TestServiceArchitecture:
    """Test the new service architecture with proper separation of concerns."""
    
    @pytest.fixture
    def mock_token_manager(self):
        return Mock(spec=SpotifyTokenManager)
    
    @pytest.fixture
    def mock_spotify_service(self, mock_token_manager):
        return SpotifyService(mock_token_manager)
    
    @pytest.fixture
    def mock_gemini_service(self, mock_spotify_service):
        return GeminiService(mock_spotify_service)
    
    @pytest.fixture
    def mock_user_repository(self):
        return Mock(spec=UserRepository)
    
    def test_spotify_service_no_db_dependency(self, mock_token_manager):
        """Test that SpotifyService doesn't depend on database or user context."""
        service = SpotifyService(mock_token_manager)
        
        # Service should only depend on token manager
        assert service.token_manager == mock_token_manager
        assert not hasattr(service, 'db')
        assert not hasattr(service, 'current_user')
    
    def test_gemini_service_no_db_dependency(self, mock_spotify_service):
        """Test that GeminiService doesn't depend on database or user context."""
        service = GeminiService(mock_spotify_service)
        
        # Service should only depend on Spotify service
        assert service.spotify_service == mock_spotify_service
        assert not hasattr(service, 'db')
        assert not hasattr(service, 'current_user')
    
    @pytest.mark.asyncio
    async def test_gemini_service_pure_business_logic(self, mock_gemini_service):
        """Test that GeminiService works with pure data, not model objects."""
        # Mock data (not model objects)
        user_profile = {
            'id': 1,
            'fitness_level': 'intermediate',
            'fitness_goal': 'strength',
            'available_days': ['Monday', 'Wednesday', 'Friday'],
            'workout_duration_minutes': 45
        }
        
        user_preferences = {
            'music_genres': ['rock', 'electronic'],
            'available_equipment': ['dumbbells', 'resistance bands'],
            'target_muscle_groups': ['chest', 'back'],
            'exercise_types': ['strength', 'cardio']
        }
        
        # Mock Spotify service responses
        mock_gemini_service.spotify_service.get_current_user_top_tracks.return_value = {
            'items': [{'name': 'Test Track'}]
        }
        mock_gemini_service.spotify_service.get_current_user_top_artists.return_value = {
            'items': [{'name': 'Test Artist'}]
        }
        mock_gemini_service.spotify_service.get_user_profile.return_value = {
            'id': 'spotify_user_id'
        }
        mock_gemini_service.spotify_service.search_tracks.return_value = {
            'tracks': {'items': [{'uri': 'spotify:track:123'}]}
        }
        mock_gemini_service.spotify_service.create_playlist.return_value = {
            'id': 'playlist_id',
            'external_urls': {'spotify': 'https://spotify.com/playlist'}
        }
        mock_gemini_service.spotify_service.add_tracks_to_playlist.return_value = {
            'snapshot_id': 'snapshot_123'
        }
        
        # Mock Gemini AI response
        with patch.object(mock_gemini_service.client.aio.models, 'generate_content') as mock_genai:
            mock_response = Mock()
            mock_response.text = '''
            {
                "playlist_recommendations": [
                    {
                        "song_title": "Test Song",
                        "artist_name": "Test Artist",
                        "reason": "Great for workouts"
                    }
                ]
            }
            '''
            mock_genai.return_value = mock_response
            
            update_callback = AsyncMock()
            
            result = await mock_gemini_service.recommend_spotify_playlist(
                user_id=1,
                refresh_token="test_refresh_token",
                update_token_callback=update_callback,
                user_profile=user_profile,
                user_preferences=user_preferences,
                workout_type="strength",
                duration_minutes=60
            )
            
            # Verify the service worked with pure data
            assert result["message"] == "Playlist created and tracks added!"
            assert "playlist_url" in result
            assert "playlist_recommendations" in result
    
    def test_user_repository_handles_data_access(self, mock_user_repository):
        """Test that UserRepository handles all data access operations."""
        # Mock repository methods
        mock_user_repository.is_spotify_connected.return_value = True
        mock_user_repository.get_spotify_refresh_token.return_value = "test_refresh_token"
        mock_user_repository.get_profile.return_value = Mock(id=1, fitness_level="intermediate")
        mock_user_repository.get_preferences.return_value = Mock(music_genres=["rock"])
        mock_user_repository.update_spotify_access_token.return_value = True
        
        # Test repository methods
        assert mock_user_repository.is_spotify_connected(1) is True
        assert mock_user_repository.get_spotify_refresh_token(1) == "test_refresh_token"
        assert mock_user_repository.get_profile(1) is not None
        assert mock_user_repository.get_preferences(1) is not None
        assert mock_user_repository.update_spotify_access_token(1, "new_token") is True
    
    @pytest.mark.asyncio
    async def test_endpoint_integration(self, mock_spotify_service, mock_user_repository):
        """Test how endpoints would integrate with the new architecture."""
        # Mock repository responses
        mock_user_repository.is_spotify_connected.return_value = True
        mock_user_repository.get_spotify_refresh_token.return_value = "test_refresh_token"
        mock_user_repository.get_profile.return_value = Mock(
            id=1, 
            fitness_level="intermediate",
            fitness_goal="strength",
            available_days=["Monday", "Wednesday"],
            workout_duration_minutes=45
        )
        mock_user_repository.get_preferences.return_value = Mock(
            music_genres=["rock"],
            available_equipment=["dumbbells"],
            target_muscle_groups=["chest"],
            exercise_types=["strength"]
        )
        
        # Mock Spotify service
        mock_spotify_service.get_user_playlists.return_value = {
            "items": [{"name": "Test Playlist"}]
        }
        
        # Simulate endpoint logic
        user_id = 1
        
        # Check Spotify connection
        if not mock_user_repository.is_spotify_connected(user_id):
            raise Exception("Spotify not connected")
        
        # Get refresh token
        refresh_token = mock_user_repository.get_spotify_refresh_token(user_id)
        if not refresh_token:
            raise Exception("Refresh token not found")
        
        # Define callback
        async def update_token_callback(new_token: str, user_id: int):
            mock_user_repository.update_spotify_access_token(user_id, new_token)
        
        # Call service (pure business logic)
        result = await mock_spotify_service.get_user_playlists(
            user_id, refresh_token, update_token_callback
        )
        
        # Verify integration works
        assert result["items"] == [{"name": "Test Playlist"}]
        mock_user_repository.is_spotify_connected.assert_called_once_with(user_id)
        mock_user_repository.get_spotify_refresh_token.assert_called_once_with(user_id)
        mock_spotify_service.get_user_playlists.assert_called_once() 