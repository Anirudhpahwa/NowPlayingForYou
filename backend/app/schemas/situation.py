from pydantic import BaseModel, Field
from typing import Literal


EnergyLevel = Literal["low", "medium", "medium-high", "high"]


class SituationProfile(BaseModel):
    """
    Structured representation of user's current situation.
    """
    raw_text: str = Field(..., description="Original user input")
    emotions: list[str] = Field(default_factory=list, description="Extracted emotions")
    energy: EnergyLevel = Field(default="medium", description="Energy level")
    settings: list[str] = Field(default_factory=list, description="Physical/social contexts")
    intents: list[str] = Field(default_factory=list, description="What user wants from music")


class AnalyzeSituationRequest(BaseModel):
    situation: str = Field(..., description="Natural language description of user's situation")


class AnalyzeSituationResponse(BaseModel):
    situation_profile: SituationProfile
