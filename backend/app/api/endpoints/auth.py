from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.schemas.token import Token

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
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

@router.post("/spotify/callback")
def spotify_callback(code: str, state: str = None, db: Session = Depends(get_db)):
    """
    Handle Spotify OAuth callback.
    """
    # This is a placeholder for the Spotify OAuth callback
    # In a real implementation, we would:
    # 1. Exchange the code for an access token
    # 2. Store the token in the user's preferences
    # 3. Redirect the user back to the app
    
    return {"message": "Spotify authentication successful"}
