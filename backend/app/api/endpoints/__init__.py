from fastapi import APIRouter
from app.api.endpoints import users, auth, profiles, workouts, playlists

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
