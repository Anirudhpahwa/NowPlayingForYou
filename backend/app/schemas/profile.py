from pydantic import BaseModel, Field
from typing import Literal


EnergyLevel = Literal["low", "medium", "medium-high", "high"]


class UserTasteProfile(BaseModel):
    id: str = Field(..., description="Unique profile identifier")
    name: str = Field(..., description="Human-readable profile name")
    top_genres: list[str] = Field(default_factory=list, description="User's top genres")
    top_artists: list[str] = Field(default_factory=list, description="User's favorite artists")
    preferred_energy: EnergyLevel = Field(default="medium", description="Preferred music energy")
    preferred_mood: list[str] = Field(default_factory=list, description="Preferred moods")
    listening_frequency: str = Field(default="casual", description="How often user listens")
    preferred_vibes: list[str] = Field(default_factory=list, description="Preferred vibe tags")


MOCK_TASTE_PROFILES: list[UserTasteProfile] = [
    UserTasteProfile(
        id="pop_enthusiast",
        name="Pop Fan",
        top_genres=["pop", "dance", "electronic"],
        top_artists=["The Weeknd", "Dua Lipa", "Taylor Swift"],
        preferred_energy="medium-high",
        preferred_mood=["euphoric", "confident", "romantic"],
        listening_frequency="enthusiast",
        preferred_vibes=["synth", "upbeat", "anthem"]
    ),
    UserTasteProfile(
        id="indie_lover",
        name="Indie Vibes",
        top_genres=["indie", "alternative", "rock"],
        top_artists=["Arctic Monkeys", "Tame Impala", "The 1975"],
        preferred_energy="medium",
        preferred_mood=["dreamy", "nostalgic", "reflective"],
        listening_frequency="regular",
        preferred_vibes=["atmospheric", "synth", "retro"]
    ),
    UserTasteProfile(
        id="hip_hop_head",
        name="Hip-Hop Head",
        top_genres=["hip-hop", "rap", "r&b"],
        top_artists=["Kendrick Lamar", "J. Cole", "Drake"],
        preferred_energy="high",
        preferred_mood=["determined", "confident", "intense"],
        listening_frequency="enthusiast",
        preferred_vibes=["bass", "hard-hitting", "lyrical"]
    ),
    UserTasteProfile(
        id="chill_listener",
        name="Chill Vibes",
        top_genres=["ambient", "lo-fi", "acoustic"],
        top_artists=["Bon Iver", "Mac DeMarco", "Khruangbin"],
        preferred_energy="low",
        preferred_mood=["calm", "peaceful", "reflective"],
        listening_frequency="casual",
        preferred_vibes=["organic", "mellow", "acoustic"]
    ),
    UserTasteProfile(
        id="rock_lover",
        name="Rock Energy",
        top_genres=["rock", "alternative rock", "hard rock"],
        top_artists=["Foo Fighters", "Arctic Monkeys", "Red Hot Chili Peppers"],
        preferred_energy="high",
        preferred_mood=["powerful", "energetic", "determined"],
        listening_frequency="regular",
        preferred_vibes=["guitar-driven", "anthemic", "high-energy"]
    ),
    UserTasteProfile(
        id="rnb_soul",
        name="R&B Soul",
        top_genres=["r&b", "soul", "neo-soul"],
        top_artists=["SZA", "Frank Ocean", "The Weeknd"],
        preferred_energy="medium",
        preferred_mood=["romantic", "reflective", "smooth"],
        listening_frequency="regular",
        preferred_vibes=["smooth", "mellow", "sensual"]
    ),
]
