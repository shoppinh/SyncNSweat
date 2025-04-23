from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, ARRAY, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(DateTime(timezone=True), index=True)
    focus = Column(String)  # e.g., "Upper Body", "Lower Body", "Push", "Pull", "Legs"
    duration_minutes = Column(Integer)
    playlist_id = Column(String, nullable=True)  # Spotify playlist ID
    playlist_name = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"))
    exercise_id = Column(String)  # ID from external exercise API
    name = Column(String)
    description = Column(Text, nullable=True)
    muscle_group = Column(String)
    equipment = Column(String, nullable=True)
    sets = Column(Integer)
    reps = Column(String)  # Could be "8-12" or just "10"
    rest_seconds = Column(Integer)
    order = Column(Integer)  # Order in the workout

    # For tracking progress
    completed_sets = Column(Integer, default=0)
    weights_used = Column(ARRAY(String), default=[])  # e.g., ["20kg", "22.5kg", "25kg"]

    # Relationships
    workout = relationship("Workout", back_populates="exercises")
