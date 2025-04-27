from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class ExerciseBase(BaseModel):
    name: str
    instructions: Optional[List[str]] = None
    target: str
    secondary_muscles: Optional[List[str]] = None
    gif_url: Optional[str] = None
    equipment: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    name: str

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: str
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True,from_attributes=True)

class WorkoutExerciseBase(ExerciseBase):
    exercise_id: int
    order: int
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True,from_attributes=True)

