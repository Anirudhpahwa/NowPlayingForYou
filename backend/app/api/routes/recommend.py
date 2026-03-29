from typing import Optional

from fastapi import APIRouter, HTTPException

from app.schemas.profile import MOCK_TASTE_PROFILES, UserTasteProfile
from app.schemas.situation import AnalyzeSituationRequest, AnalyzeSituationResponse, SituationProfile
from app.schemas.response import ProfileListResponse, RecommendResponse, RecommendationResult, Song
from app.services.situation_analyzer import SituationAnalyzer
from app.services.recommender import recommend

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


@router.post("/recommend", response_model=RecommendResponse)
def recommend_songs(request: dict):
    """
    Get song recommendations based on situation and optional taste profile.
    
    Request body:
    {
      "situation": "I'm in the metro going to meet my crush...",
      "profile_id": "optional_profile_id"
    }
    """
    situation_text = request.get("situation")
    profile_id = request.get("profile_id")
    
    if not situation_text:
        raise HTTPException(status_code=400, detail="situation is required")
    
    try:
        # Analyze situation
        analyzer = get_situation_analyzer()
        situation = analyzer.analyze(situation_text)
        
        # Get taste profile if provided
        taste = None
        if profile_id:
            for p in MOCK_TASTE_PROFILES:
                if p.id == profile_id:
                    taste = p
                    break
        
        # Get recommendations
        recommendations = recommend(situation, taste, limit=8)
        
        # Convert to response format (with placeholder "why" - will add AI later)
        results = []
        for rec in recommendations:
            results.append(RecommendationResult(
                song=rec["song"],
                score=rec["score"],
                why=_generate_why(rec["song"], situation, taste if taste else None)
            ))
        
        return RecommendResponse(
            recommendations=results,
            situation_analysis={
                "emotions": situation.emotions,
                "energy": situation.energy,
                "settings": situation.settings,
                "intents": situation.intents
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


def _generate_why(song: Song, situation: SituationProfile, taste: Optional[UserTasteProfile] = None) -> str:
    """Generate a simple 'why' explanation (placeholder - can be AI-enhanced later)."""
    reasons = []
    
    # Energy match
    if song.energy == situation.energy:
        reasons.append(f"matches your {situation.energy} energy")
    
    # Emotion match
    matching_moods = set(song.moods) & set(situation.emotions)
    if matching_moods:
        reasons.append(f"captures the {list(matching_moods)[0]} mood")
    
    # Setting match
    matching_settings = set(song.situations or []) & set(situation.settings)
    if matching_settings:
        reasons.append(f"perfect for {list(matching_settings)[0]}")
    
    # Genre match from taste
    if taste:
        matching_genres = set(song.genres) & set(taste.top_genres)
        if matching_genres:
            reasons.append(f"fits your love of {list(matching_genres)[0]}")
    
    if not reasons:
        reasons.append("a great fit for this moment")
    
    return reasons[0].capitalize() + "."


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
