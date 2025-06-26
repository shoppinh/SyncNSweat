from fastapi import Depends
from app.services.spotify import SpotifyService
from app.services.spotify_token_manager import SpotifyTokenManager
from app.repositories.user_repository import UserRepository
from app.core.config import settings
from app.db.session import get_db
from sqlalchemy.orm import Session
import redis


def get_redis_client():
    """Get Redis client instance"""
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=False)


def get_token_manager(redis_client=Depends(get_redis_client)):
    """Get Spotify token manager instance"""
    return SpotifyTokenManager(redis_client)


def get_spotify_service(token_manager=Depends(get_token_manager)):
    """Get Spotify service instance with dependency injection"""
    return SpotifyService(token_manager)


def get_user_repository(db: Session = Depends(get_db)):
    """Get user repository instance"""
    return UserRepository(db) 