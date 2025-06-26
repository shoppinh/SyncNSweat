import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import redis
from app.core.config import settings


class SpotifyTokenManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.token_prefix = "spotify_token:"
        self.expiry_buffer = 300  # 5 minutes buffer
    
    def get_cached_token(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get cached token from Redis"""
        key = f"{self.token_prefix}{user_id}"
        token_data = self.redis.get(key)
        if token_data:
            return json.loads(token_data.decode('utf-8'))
        return None
    
    def cache_token(self, user_id: int, token_data: Dict[str, Any], expires_in: int):
        """Cache token with expiration"""
        key = f"{self.token_prefix}{user_id}"
        # Cache for slightly less than actual expiry to ensure fresh tokens
        cache_duration = expires_in - self.expiry_buffer
        self.redis.setex(key, cache_duration, json.dumps(token_data))
    
    def is_token_expired(self, token_data: Dict[str, Any]) -> bool:
        """Check if token is expired or close to expiry"""
        if 'expires_at' not in token_data:
            return True
        return datetime.now() > datetime.fromisoformat(token_data['expires_at'])
    
    def invalidate_token(self, user_id: int):
        """Remove cached token"""
        key = f"{self.token_prefix}{user_id}"
        self.redis.delete(key) 