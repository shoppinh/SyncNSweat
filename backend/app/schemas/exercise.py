from pydantic import BaseModel
from typing import List, Optional, Union

class WorkoutExerciseBase(BaseModel):
    exercise_id: str
    name: str
    description: Optional[str] = None
    muscle_group: str
    equipment: Optional[str] = None
    sets: int
    reps: str
    rest_seconds: int
    completed_sets: Optional[int] = 0
    weights_used: Optional[List[str]] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExerciseUpdate(BaseModel):
    completed_sets: Optional[int] = None
    weights_used: Optional[List[str]] = None

class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    workout_id: int
    order: int

    class Config:
        orm_mode = True
