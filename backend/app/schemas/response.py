from pydantic import BaseModel


class Song(BaseModel):
    id: str
    title: str
    artist: str
    genres: list[str]
    moods: list[str]
    energy: str
    spotify_url: str
    situations: list[str] = []
    vibes: list[str] = []
    vibe_tags: list[str] = []


class RecommendationResult(BaseModel):
    song: Song
    score: float
    why: str


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationResult]
    situation_analysis: dict | None = None


class ProfileListResponse(BaseModel):
    profiles: list[dict]
