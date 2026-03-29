from fastapi import APIRouter

from app.schemas.profile import MOCK_TASTE_PROFILES, UserTasteProfile
from app.schemas.response import ProfileListResponse

router = APIRouter()


@router.get("/profiles", response_model=ProfileListResponse)
def get_taste_profiles():
    """Get list of available mock taste profiles (for dev/testing only)."""
    return ProfileListResponse(profiles=[p.model_dump() for p in MOCK_TASTE_PROFILES])


@router.get("/profiles/{profile_id}", response_model=UserTasteProfile)
def get_taste_profile(profile_id: str):
    """Get a specific taste profile by ID (for dev/testing only)."""
    for profile in MOCK_TASTE_PROFILES:
        if profile.id == profile_id:
            return profile
    return {"error": "Profile not found"}
