# Service Architecture - Clean Architecture Implementation

## Overview

This document describes the refactored service architecture that follows clean architecture principles and proper separation of concerns. The new architecture eliminates tight coupling between services and data access layers.

## Architecture Principles

### 1. **Separation of Concerns**
- **Services**: Pure business logic, no database or HTTP context dependencies
- **Repositories**: Handle all data access operations
- **Endpoints**: Orchestrate between repositories and services
- **Dependencies**: Injected via FastAPI dependency injection

### 2. **Dependency Inversion**
- Services depend on abstractions, not concrete implementations
- Database sessions and user context are handled at the endpoint level
- Services receive data as parameters, not through direct database access

### 3. **Single Responsibility**
- Each class has one clear purpose
- Services focus on business logic
- Repositories focus on data access
- Endpoints focus on HTTP concerns

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Endpoints                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Auth Routes   │  │ Playlist Routes │  │ Other Routes │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Dependency Injection                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ UserRepository  │  │ SpotifyService  │  │ TokenManager │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ SpotifyService  │  │ GeminiService   │  │ Other Services│ │
│  │ (Pure Logic)    │  │ (Pure Logic)    │  │ (Pure Logic) │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ UserRepository  │  │ TokenManager    │  │ Redis Cache  │ │
│  │ (SQLAlchemy)    │  │ (Redis)         │  │ (External)   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. **UserRepository**
```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
    
    def get_spotify_refresh_token(self, user_id: int) -> Optional[str]:
        """Get user's Spotify refresh token"""
    
    def update_spotify_access_token(self, user_id: int, new_access_token: str) -> bool:
        """Update user's Spotify access token"""
```

**Responsibilities:**
- All database operations for user data
- Spotify token management
- Profile and preferences access

### 2. **SpotifyService**
```python
class SpotifyService:
    def __init__(self, token_manager: SpotifyTokenManager):
        self.token_manager = token_manager
    
    async def get_user_playlists(self, user_id: int, refresh_token: str, 
                                update_callback: Callable) -> Dict[str, Any]:
        """Pure business logic - no database dependencies"""
```

**Responsibilities:**
- Spotify API interactions
- Token refresh logic
- Playlist management
- **No database or user context dependencies**

### 3. **GeminiService**
```python
class GeminiService:
    def __init__(self, spotify_service: SpotifyService):
        self.spotify_service = spotify_service
    
    async def recommend_spotify_playlist(self, user_id: int, refresh_token: str,
                                       update_callback: Callable, user_profile: Dict[str, Any],
                                       user_preferences: Dict[str, Any], workout_type: str,
                                       duration_minutes: int) -> Dict[str, Any]:
        """Pure business logic - works with data, not models"""
```

**Responsibilities:**
- AI-powered recommendations
- Playlist generation logic
- **No database or user context dependencies**
- **Works with pure data, not model objects**

## Usage Examples

### Endpoint Implementation
```python
@router.get("/spotify/recommendations")
async def get_spotify_recommendations(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
    spotify_service: SpotifyService = Depends(get_spotify_service),
):
    # 1. Data access via repository
    if not user_repository.is_spotify_connected(current_user.id):
        raise HTTPException(status_code=400, detail="Spotify not connected")
    
    refresh_token = user_repository.get_spotify_refresh_token(current_user.id)
    profile = user_repository.get_profile(current_user.id)
    preferences = user_repository.get_preferences(current_user.id)
    
    # 2. Define callback for token updates
    async def update_token_callback(new_token: str, user_id: int):
        user_repository.update_spotify_access_token(user_id, new_token)
    
    # 3. Convert models to data for service
    profile_data = {
        'id': profile.id,
        'fitness_level': profile.fitness_level,
        # ... other fields
    }
    
    # 4. Call service with pure business logic
    gemini_service = GeminiService(spotify_service)
    recommendations = await gemini_service.recommend_spotify_playlist(
        user_id=current_user.id,
        refresh_token=refresh_token,
        update_token_callback=update_token_callback,
        user_profile=profile_data,
        user_preferences=preferences_data,
        workout_type=workout_type,
        duration_minutes=duration_minutes
    )
    
    return recommendations
```

### Service Testing
```python
def test_gemini_service_pure_business_logic():
    """Test that GeminiService works with pure data, not model objects."""
    # Mock data (not model objects)
    user_profile = {
        'id': 1,
        'fitness_level': 'intermediate',
        'fitness_goal': 'strength',
    }
    
    user_preferences = {
        'music_genres': ['rock', 'electronic'],
        'available_equipment': ['dumbbells'],
    }
    
    # Service works with pure data
    result = await gemini_service.recommend_spotify_playlist(
        user_id=1,
        refresh_token="test_token",
        update_token_callback=mock_callback,
        user_profile=user_profile,
        user_preferences=user_preferences,
        workout_type="strength",
        duration_minutes=60
    )
    
    assert result["message"] == "Playlist created and tracks added!"
```

## Benefits

### 1. **Testability**
- Services can be tested in isolation
- Easy to mock dependencies
- No database setup required for service tests

### 2. **Maintainability**
- Clear boundaries between layers
- Single responsibility principle
- Easy to modify business logic without affecting data access

### 3. **Reusability**
- Services can be used in different contexts (API, background jobs, CLI)
- No tight coupling to HTTP context
- Pure business logic is framework-agnostic

### 4. **Scalability**
- Services can be easily moved to microservices
- Clear interfaces between components
- Easy to add caching, monitoring, etc.

## Migration Guide

### Before (Anti-pattern)
```python
class SpotifyService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
    
    async def get_user_playlists(self):
        # Direct database access in service
        preferences = self.db.query(Preferences).filter(...).first()
        # Business logic mixed with data access
```

### After (Clean Architecture)
```python
class SpotifyService:
    def __init__(self, token_manager: SpotifyTokenManager):
        self.token_manager = token_manager
    
    async def get_user_playlists(self, user_id: int, refresh_token: str, 
                                update_callback: Callable) -> Dict[str, Any]:
        # Pure business logic
        return await self._make_authenticated_request(...)

# In endpoint:
user_repository = UserRepository(db)
refresh_token = user_repository.get_spotify_refresh_token(current_user.id)
playlists = await spotify_service.get_user_playlists(
    current_user.id, refresh_token, update_callback
)
```

## Best Practices

### 1. **Service Design**
- Never inject `db` or `current_user` into services
- Services should receive all data as parameters
- Use callbacks for side effects (like token updates)

### 2. **Repository Design**
- Handle all data access operations
- Provide clean interfaces for services
- Handle database transactions and error handling

### 3. **Endpoint Design**
- Orchestrate between repositories and services
- Handle HTTP-specific concerns (status codes, headers)
- Convert between model objects and service data

### 4. **Testing Strategy**
- Test services with pure data
- Mock repositories for service tests
- Test repositories with real database
- Integration tests for endpoints

## Future Enhancements

1. **Interface Abstractions**: Define interfaces for repositories and services
2. **Event-Driven Architecture**: Add event publishing for side effects
3. **CQRS Pattern**: Separate read and write operations
4. **Domain Events**: Add domain events for business logic coordination
5. **Validation Layer**: Add input validation at service boundaries 