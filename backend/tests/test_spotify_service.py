import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.spotify import SpotifyService
from app.core.config import settings

class TestSpotifyService(unittest.TestCase):
    def setUp(self):
        self.spotify_service = SpotifyService()
        self.test_code = "test_code"
        self.test_redirect_uri = "http://localhost:8000/callback"
    
    def test_get_auth_url(self):
        # Test without state
        auth_url = self.spotify_service.get_auth_url(self.test_redirect_uri)
        self.assertIn("client_id=", auth_url)
        self.assertIn("response_type=code", auth_url)
        self.assertIn(f"redirect_uri={self.test_redirect_uri}", auth_url)
        self.assertIn("scope=", auth_url)
        
        # Test with state
        state = "test_state"
        auth_url_with_state = self.spotify_service.get_auth_url(self.test_redirect_uri, state)
        self.assertIn(f"state={state}", auth_url_with_state)
    
    @patch('requests.post')
    def test_get_access_token(self, mock_post):
        # Mock the response from the Spotify API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "test_refresh_token"
        }
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.spotify_service.get_access_token(self.test_code, self.test_redirect_uri)
        
        # Check the result
        self.assertEqual(result["access_token"], "test_access_token")
        self.assertEqual(result["token_type"], "Bearer")
        self.assertEqual(result["expires_in"], 3600)
        self.assertEqual(result["refresh_token"], "test_refresh_token")
        
        # Check that the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://accounts.spotify.com/api/token")
        self.assertIn("Authorization", kwargs["headers"])
        self.assertEqual(kwargs["data"]["grant_type"], "authorization_code")
        self.assertEqual(kwargs["data"]["code"], self.test_code)
        self.assertEqual(kwargs["data"]["redirect_uri"], self.test_redirect_uri)
    
    @patch('requests.post')
    def test_refresh_access_token(self, mock_post):
        # Mock the response from the Spotify API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.spotify_service.refresh_access_token("test_refresh_token")
        
        # Check the result
        self.assertEqual(result["access_token"], "new_access_token")
        self.assertEqual(result["token_type"], "Bearer")
        self.assertEqual(result["expires_in"], 3600)
        
        # Check that the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://accounts.spotify.com/api/token")
        self.assertIn("Authorization", kwargs["headers"])
        self.assertEqual(kwargs["data"]["grant_type"], "refresh_token")
        self.assertEqual(kwargs["data"]["refresh_token"], "test_refresh_token")
    
    @patch('requests.get')
    def test_get_user_profile(self, mock_get):
        # Mock the response from the Spotify API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test_user_id",
            "display_name": "Test User",
            "email": "test@example.com"
        }
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.spotify_service.get_user_profile("test_access_token")
        
        # Check the result
        self.assertEqual(result["id"], "test_user_id")
        self.assertEqual(result["display_name"], "Test User")
        self.assertEqual(result["email"], "test@example.com")
        
        # Check that the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://api.spotify.com/v1/me")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_access_token")

if __name__ == '__main__':
    unittest.main()
