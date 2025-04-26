from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
