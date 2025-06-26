# Spotify Service Improvements

## Overview

The Spotify service has been completely refactored to improve performance, code readability, and maintainability. The new implementation follows FastAPI best practices and includes proper async patterns, token caching, and dependency injection.

## Key Improvements

### 1. Token Management & Caching

- **Redis-based token caching**: Tokens are cached in Redis to reduce database calls and API requests
- **Automatic token refresh**: Tokens are automatically refreshed when expired
- **Configurable cache TTL**: Token cache duration is configurable with a 5-minute buffer

### 2. Async/Await Patterns

- **Consistent async usage**: All Spotify API calls are now properly async
- **HTTPX client**: Replaced `requests` with `httpx` for better async support
- **Connection pooling**: Proper HTTP client lifecycle management

### 3. Dependency Injection

- **Service injection**: Spotify service is injected via FastAPI dependencies
- **Token manager injection**: Separate token manager for better separation of concerns
- **Testability**: Services are easier to mock and test

### 4. Error Handling & Retry Logic

- **Exponential backoff**: Automatic retry with exponential backoff for failed requests
- **Configurable retries**: Number of retry attempts is configurable
- **Better error messages**: More descriptive error messages for debugging

### 5. Code Organization

- **Single responsibility**: Each class has a clear, single purpose
- **Type hints**: Complete type annotations throughout
- **Configuration**: Centralized settings management

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  SpotifyService  │    │ TokenManager    │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Dependencies │ │───▶│ │ Token Cache  │ │───▶│ │ Redis Cache │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │   Endpoints  │ │───▶│ │ API Requests │ │───▶│ │ Token Refresh│ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Usage

### Basic Usage

```python
from app.dependencies.spotify import get_spotify_service
from app.services.spotify import SpotifyService

@router.get("/spotify/playlists")
async def get_user_playlists(
    current_user: User = Depends(get_current_user),
    spotify_service: SpotifyService = Depends(get_spotify_service),
):
    # Define callback for token updates
    async def update_token_callback(new_token: str, user_id: int):
        # Update token in database
        pass
    
    # Get user playlists with automatic token management
    playlists = await spotify_service.get_user_playlists(
        current_user.id, 
        refresh_token, 
        update_token_callback
    )
    return playlists
```

### Token Management

```python
from app.services.spotify_token_manager import SpotifyTokenManager

# Token manager handles caching and expiration
token_manager = SpotifyTokenManager(redis_client)

# Cache a token
token_manager.cache_token(user_id, token_data, expires_in)

# Check if token is expired
if token_manager.is_token_expired(token_data):
    # Refresh token
    pass
```

## Configuration

Add these settings to your environment:

```bash
# Redis configuration
REDIS_URL=redis://localhost:6379

# Spotify token settings
SPOTIFY_TOKEN_CACHE_TTL=3300  # 55 minutes (5 min buffer)
SPOTIFY_REQUEST_TIMEOUT=30
SPOTIFY_MAX_RETRIES=3
```

## Performance Benefits

1. **Reduced API calls**: Token caching reduces Spotify API requests
2. **Faster response times**: Cached tokens eliminate token refresh delays
3. **Better resource utilization**: Connection pooling and async operations
4. **Improved reliability**: Retry logic handles transient failures

## Migration Guide

### For Existing Code

1. **Update dependencies**: Add Redis to requirements.txt
2. **Update service initialization**: Use dependency injection instead of direct instantiation
3. **Update method calls**: Use new async methods with user_id and callback parameters
4. **Add token update callbacks**: Implement callbacks to update tokens in your database

### Example Migration

**Before:**
```python
spotify_service = SpotifyService(db, current_user)
playlists = await spotify_service.get_user_playlists(access_token, refresh_token)
```

**After:**
```python
spotify_service: SpotifyService = Depends(get_spotify_service)

async def update_token_callback(new_token: str, user_id: int):
    # Update token in database
    pass

playlists = await spotify_service.get_user_playlists(
    current_user.id, refresh_token, update_token_callback
)
```

## Testing

The new implementation includes comprehensive tests:

```bash
# Run Spotify service tests
pytest tests/test_spotify_service_improved.py -v

# Run with coverage
pytest tests/test_spotify_service_improved.py --cov=app.services.spotify
```

## Monitoring

Monitor these metrics for optimal performance:

- Token cache hit rate
- Token refresh frequency
- API request latency
- Error rates and retry attempts

## Troubleshooting

### Common Issues

1. **Redis connection errors**: Ensure Redis is running and accessible
2. **Token refresh failures**: Check Spotify API credentials and refresh token validity
3. **High latency**: Monitor cache hit rates and adjust TTL settings

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.getLogger('app.services.spotify').setLevel(logging.DEBUG)
```

## Future Enhancements

1. **Token rotation**: Implement automatic token rotation for security
2. **Rate limiting**: Add rate limiting to prevent API quota exhaustion
3. **Metrics collection**: Add detailed metrics for monitoring and optimization
4. **Circuit breaker**: Implement circuit breaker pattern for API resilience 