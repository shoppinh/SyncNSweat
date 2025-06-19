from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
)
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.spotify import SpotifyService

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if user with this email already exists
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create profile for user if name is provided
    if user_in.name:
        profile = Profile(user_id=db_user.id, name=user_in.name)
        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Create empty preferences
        preferences = Preferences(profile_id=profile.id)
        db.add(preferences)
        db.commit()

    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    return login(form_data, db)


@router.post("/refresh-token", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/spotify/callback/")
def spotify_callback(
    code: str = Query(None, description="Spotify authorization code"),
    state: str = Query(None, description="State parameter (user ID)"),
    error: str = Query(None, description="Spotify error, if any"),
    db: Session = Depends(get_db),
):
    """
    Handle Spotify OAuth callback.
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Spotify authentication error: {error}",
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code is required",
        )

    # Get user ID from state parameter
    if not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="State parameter is required",
        )

    try:
        user_id = int(state)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter"
        )

    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Get user profile
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    # Get user preferences
    preferences = (
        db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    )
    if not preferences:
        # Create preferences if they don't exist
        preferences = Preferences(profile_id=profile.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)

    # Exchange code for access token
    spotify_service = SpotifyService()
    redirect_uri = f"{settings.SPOTIFY_REDIRECT_URL}/api/v1/auth/spotify/callback"
    token_data = spotify_service.get_access_token(code, redirect_uri)

    if "error" in token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Spotify token error: {token_data['error']}",
        )

    # Store token in user preferences
    preferences.spotify_connected = True
    preferences.spotify_data = {
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in"),
        "token_type": token_data.get("token_type"),
    }

    db.add(preferences)
    db.commit()

    # Return success message with redirect URL
    return {
        "message": "Spotify authentication successful",
        "redirect_url": "syncnsweat://spotify-callback?success=true",
    }
