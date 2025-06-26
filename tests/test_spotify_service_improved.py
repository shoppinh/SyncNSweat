import pytest
from unittest.mock import Mock, patch, AsyncMock
import json
from datetime import datetime, timedelta

from app.services.spotify import SpotifyService
from app.services.spotify_token_manager import SpotifyTokenManager


class TestSpotifyTokenManager:
    def test_cache_and_retrieve_token(self):
        """Test token caching and retrieval"""
        mock_redis = Mock()
        token_manager = SpotifyTokenManager(mock_redis)
        
        user_id = 1
        token_data = {
            "access_token": "test_token",
            "expires_in": 3600,
            "expires_at": datetime.now().isoformat()
        }
        
        # Test caching
        token_manager.cache_token(user_id, token_data, 3600)
        mock_redis.setex.assert_called_once()
        
        # Test retrieval
        mock_redis.get.return_value = json.dumps(token_data).encode('utf-8')
        cached_token = token_manager.get_cached_token(user_id)
        assert cached_token == token_data
    
    def test_token_expiration_check(self):
        """Test token expiration logic"""
        mock_redis = Mock()
        token_manager = SpotifyTokenManager(mock_redis)
        
        # Test expired token
        expired_token = {
            "access_token": "test_token",
            "expires_at": (datetime.now() - timedelta(hours=1)).isoformat()
        }
        assert token_manager.is_token_expired(expired_token) is True
        
        # Test valid token
        valid_token = {
            "access_token": "test_token",
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        assert token_manager.is_token_expired(valid_token) is False


class TestSpotifyService:
    @pytest.fixture
    def mock_token_manager(self):
        return Mock(spec=SpotifyTokenManager)
    
    @pytest.fixture
    def spotify_service(self, mock_token_manager):
        return SpotifyService(mock_token_manager)
    
    def test_get_auth_url(self, spotify_service):
        """Test authorization URL generation"""
        redirect_uri = "http://localhost:8000/callback"
        state = "test_state"
        
        auth_url = spotify_service.get_auth_url(redirect_uri, state)
        
        assert "client_id=" in auth_url
        assert "response_type=code" in auth_url
        assert f"redirect_uri={redirect_uri}" in auth_url
        assert f"state={state}" in auth_url
        assert "scope=" in auth_url
    
    @pytest.mark.asyncio
    async def test_get_access_token(self, spotify_service):
        """Test access token exchange"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await spotify_service.get_access_token("test_code", "http://localhost:8000/callback")
            
            assert result["access_token"] == "test_access_token"
            assert result["refresh_token"] == "test_refresh_token"
            assert result["expires_in"] == 3600
    
    @pytest.mark.asyncio
    async def test_token_refresh_with_retry(self, spotify_service):
        """Test token refresh with retry logic"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await spotify_service._refresh_token("test_refresh_token")
            
            assert result["access_token"] == "new_access_token"
            assert result["expires_in"] == 3600
    
    @pytest.mark.asyncio
    async def test_authenticated_request_with_token_refresh(self, spotify_service, mock_token_manager):
        """Test authenticated request with automatic token refresh"""
        # Mock cached token as expired
        mock_token_manager.get_cached_token.return_value = None
        mock_token_manager.is_token_expired.return_value = True
        
        # Mock token refresh response
        refresh_response = {
            "access_token": "new_access_token",
            "expires_in": 3600
        }
        
        # Mock API response
        api_response = {"data": "test_data"}
        
        update_callback = AsyncMock()
        
        with patch.object(spotify_service, '_refresh_token', return_value=refresh_response), \
             patch('httpx.AsyncClient') as mock_client:
            
            mock_client.return_value.__aenter__.return_value.request.return_value.json.return_value = api_response
            
            result = await spotify_service._make_authenticated_request(
                "GET", "/test", 1, "refresh_token", update_callback
            )
            
            assert result == api_response
            update_callback.assert_called_once_with("new_access_token", 1)
            mock_token_manager.cache_token.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_token_manager):
        """Test async context manager functionality"""
        async with SpotifyService(mock_token_manager) as service:
            assert service._client is not None
        
        # Client should be closed after context exit
        assert service._client is None 