from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

from pydantic.alias_generators import to_camel
from app.schemas.exercise import ExerciseResponse, WorkoutExerciseCreate

class WorkoutBase(BaseModel):
    date: Optional[datetime] = None
    focus: Optional[str] = None
    duration_minutes: Optional[int] = None
    playlist_id: Optional[str] = None
    playlist_name: Optional[str] = None
    completed: Optional[bool] = False

class WorkoutCreate(WorkoutBase):
    date: Optional[datetime] = None
    exercises: Optional[List[WorkoutExerciseCreate]] = None
    
class WorkoutSuggest(WorkoutBase):
    fitness_level: Optional[str] = None
    available_equipment: Optional[List[str]] = None

class WorkoutUpdate(WorkoutBase):
    pass



class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    created_at: datetime
    workout_exercises: List[ExerciseResponse] = []

    model_config = ConfigDict(from_attributes=True)
class WorkoutExerciseResponse(BaseModel):
    exercise_id: int
    workout_id: int
    sets: int
    reps: int
    rest_seconds: int
    order: int
    
    completed_sets: int
    weights_used: List[str]
    workout: WorkoutResponse
    exercise: ExerciseResponse
    
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True,from_attributes=True)
    
class ScheduleRequest(BaseModel):
    """Request model for generating a workout schedule."""
    regenerate: Optional[bool] = False

class ScheduleResponse(BaseModel):
    """Response model for a generated workout schedule."""
    workouts: List[WorkoutResponse]
    message: str

class UserProfile(BaseModel):
    age: int
    fitness_level: str
    goals: List[str]
    available_equipment: List[str]
    preferences: Optional[Dict[str, Any]] = None

class WorkoutAIResponse(BaseModel):
    workout_plan: Dict[str, Any]
    message: str

