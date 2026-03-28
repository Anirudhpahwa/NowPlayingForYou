from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    situation: str = Field(..., description="Natural language description of user's current situation")
    genres: list[str] = Field(default_factory=list, description="User's favorite genres")
    artists: list[str] = Field(default_factory=list, description="User's favorite artists")
