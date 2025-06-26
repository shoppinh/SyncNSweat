from typing import Optional, Dict, Any, cast
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_profile(self, user_id: int) -> Optional[Profile]:
        """Get user profile"""
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()
    
    def get_preferences(self, user_id: int) -> Optional[Preferences]:
        """Get user preferences"""
        profile = self.get_profile(user_id)
        if not profile:
            return None
        return self.db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    
    def get_spotify_refresh_token(self, user_id: int) -> Optional[str]:
        """Get user's Spotify refresh token"""
        preferences = self.get_preferences(user_id)
        if not preferences:
            return None
        spotify_data = cast(Dict[str, Any], preferences.spotify_data)
        if not spotify_data:
            return None
        return spotify_data.get("refresh_token")
    
    def update_spotify_access_token(self, user_id: int, new_access_token: str) -> bool:
        """Update user's Spotify access token"""
        preferences = self.get_preferences(user_id)
        if not preferences:
            return False
        
        # Initialize spotify_data if it doesn't exist
        spotify_data = cast(Dict[str, Any], preferences.spotify_data) or {}
        
        # Update the access token
        spotify_data["access_token"] = new_access_token
        setattr(preferences, 'spotify_data', spotify_data)
        
        self.db.add(preferences)
        self.db.commit()
        return True
    
    def get_spotify_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's complete Spotify data"""
        preferences = self.get_preferences(user_id)
        if not preferences:
            return None
        return cast(Dict[str, Any], preferences.spotify_data)
    
    def is_spotify_connected(self, user_id: int) -> bool:
        """Check if user has connected Spotify"""
        preferences = self.get_preferences(user_id)
        if not preferences:
            return False
        return bool(cast(bool, preferences.spotify_connected))