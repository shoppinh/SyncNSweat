
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.services.exercise import ExerciseService
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.workout import Exercise

router = APIRouter()

@router.post("/database/sync-external-source")
def synchronize_database(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """_summary_
    Synchronize the database with ExerciseDB API

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    
    exercise_service = ExerciseService()
    # Delete all existing exercises
    db.query(Exercise).delete()    
    db.commit()
    # Fetch all exercises from ExerciseDB API
    
    exercises = exercise_service.get_exercises(params={"limit": 1324})
    # Update Exercise table with fetched data
    db.bulk_insert_mappings(Exercise, exercises)  
        
    db.commit()
    
    return {"message": "Database synchronized successfully"}
