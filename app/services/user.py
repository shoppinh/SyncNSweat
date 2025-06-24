from http.client import HTTPException
from app.models.preferences import Preferences
from app.models.profile import Profile
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def update_access_token(self, access_token: str, current_user: UserResponse):
        profile = self.db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        preferences = self.db.query(Preferences).filter(Preferences.profile_id == profile.id).first()
        if not preferences:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Preferences not found"
            )
        
        # Update preferences fields
        setattr(preferences, 'access_token', access_token)

        self.db.add(preferences)
        self.db.commit()
        self.db.refresh(preferences)
        
        return True
        