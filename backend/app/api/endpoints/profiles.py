from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.preferences import Preferences
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from app.schemas.preferences import PreferencesCreate, PreferencesResponse, PreferencesUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=ProfileResponse)
def read_profile_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new profile for the current user.
    """
    # Check if user already has a profile
    db_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if db_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a profile"
        )
    
    # Create new profile
    db_profile = Profile(
        user_id=current_user.id,
        name=profile_in.name,
        fitness_goal=profile_in.fitness_goal,
        fitness_level=profile_in.fitness_level,
        available_days=profile_in.available_days,
        workout_duration_minutes=profile_in.workout_duration_minutes
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return db_profile

@router.put("/me", response_model=ProfileResponse)
def update_profile_me(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile fields
    for field, value in profile_in.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/me/preferences", response_model=PreferencesResponse)
def read_preferences_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's preferences.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    preferences = db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    
    return preferences

@router.post("/me/preferences", response_model=PreferencesResponse, status_code=status.HTTP_201_CREATED)
def create_preferences_me(
    preferences_in: PreferencesCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create preferences for the current user.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Check if preferences already exist
    db_preferences = db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    if db_preferences:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preferences already exist"
        )
    
    # Create new preferences
    db_preferences = Preferences(
        profile_id=profile.id,
        **preferences_in.dict()
    )
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    
    return db_preferences

@router.put("/me/preferences", response_model=PreferencesResponse)
def update_preferences_me(
    preferences_in: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's preferences.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    preferences = db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    
    # Update preferences fields
    for field, value in preferences_in.dict(exclude_unset=True).items():
        setattr(preferences, field, value)
    
    db.add(preferences)
    db.commit()
    db.refresh(preferences)
    return preferences
