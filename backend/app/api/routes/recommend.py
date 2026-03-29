from fastapi import APIRouter, HTTPException

from app.schemas.profile import MOCK_TASTE_PROFILES, UserTasteProfile
from app.schemas.situation import AnalyzeSituationRequest, AnalyzeSituationResponse, SituationProfile
from app.schemas.response import ProfileListResponse
from app.services.situation_analyzer import SituationAnalyzer

router = APIRouter()

_situation_analyzer = None


def get_situation_analyzer() -> SituationAnalyzer:
    global _situation_analyzer
    if _situation_analyzer is None:
        try:
            _situation_analyzer = SituationAnalyzer()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return _situation_analyzer


@router.post("/analyze-situation", response_model=AnalyzeSituationResponse)
def analyze_situation(request: AnalyzeSituationRequest):
    """Analyze a situation description and extract structured attributes."""
    try:
        analyzer = get_situation_analyzer()
        profile = analyzer.analyze(request.situation)
        return AnalyzeSituationResponse(situation_profile=profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


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
