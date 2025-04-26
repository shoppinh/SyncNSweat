from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.exercise import WorkoutExerciseCreate, WorkoutExerciseResponse

class WorkoutBase(BaseModel):
    date: Optional[datetime] = None
    focus: Optional[str] = None
    duration_minutes: Optional[int] = None
    playlist_id: Optional[str] = None
    playlist_name: Optional[str] = None
    completed: Optional[bool] = False

class WorkoutCreate(WorkoutBase):
    date: datetime
    exercises: Optional[List[WorkoutExerciseCreate]] = None

class WorkoutUpdate(WorkoutBase):
    pass

class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    created_at: datetime
    exercises: List[WorkoutExerciseResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ScheduleRequest(BaseModel):
    """Request model for generating a workout schedule."""
    regenerate: Optional[bool] = False

class ScheduleResponse(BaseModel):
    """Response model for a generated workout schedule."""
    workouts: List[WorkoutResponse]
    message: str
