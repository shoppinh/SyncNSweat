from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if user with this email already exists
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create profile for user if name is provided
    if user_in.name:
        profile = Profile(user_id=db_user.id, name=user_in.name)
        db.add(profile)
        db.commit()
    
    return db_user

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user.
    """
    if user_in.password:
        hashed_password = get_password_hash(user_in.password)
        current_user.hashed_password = hashed_password
    
    if user_in.email:
        # Check if email is already taken
        if user_in.email != current_user.email:
            db_user = db.query(User).filter(User.email == user_in.email).first()
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        current_user.email = user_in.email
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
