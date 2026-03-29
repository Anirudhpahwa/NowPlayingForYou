from pydantic import BaseModel, Field
from typing import Literal


EnergyLevel = Literal["low", "medium", "medium-high", "high"]


class TasteAffinity(BaseModel):
    """A single taste preference with optional affinity score."""
    value: str
    affinity: float = Field(default=1.0, ge=0.0, le=1.0, description="Strength of preference 0-1")


class TasteZone(BaseModel):
    """
    A cluster of related taste preferences.
    Represents a different 'side' of the user's music taste.
    """
    name: str = Field(..., description="Zone name, e.g., 'chill evening', 'workout mode'")
    genres: list[str] = Field(default_factory=list)
    moods: list[str] = Field(default_factory=list)
    vibes: list[str] = Field(default_factory=list)
    energy_preference: EnergyLevel = Field(default="medium")


class UserTasteProfile(BaseModel):
    """
    Multi-dimensional user taste profile.
    Supports multiple taste zones and varied affinities.
    """
    id: str = Field(..., description="Unique profile identifier")
    name: str = Field(..., description="Human-readable profile name")
    
    # Flat preferences (for simple matching)
    top_genres: list[str] = Field(default_factory=list, description="All-time favorite genres")
    top_artists: list[str] = Field(default_factory=list, description="All-time favorite artists")
    
    # Multi-dimensional taste (for context-aware matching)
    taste_zones: list[TasteZone] = Field(
        default_factory=list,
        description="Different taste clusters representing different sides of the user"
    )
    
    # Behavioral signals
    listening_frequency: str = Field(default="casual", description="How often user listens")


# Sample mock profiles with multi-dimensional taste
MOCK_TASTE_PROFILES: list[UserTasteProfile] = [
    UserTasteProfile(
        id="pop_enthusiast",
        name="Pop Fan",
        top_genres=["pop", "dance", "electronic"],
        top_artists=["The Weeknd", "Dua Lipa", "Taylor Swift", "Bad Bunny"],
        taste_zones=[
            TasteZone(
                name="Going Out",
                genres=["pop", "dance", "electronic"],
                moods=["euphoric", "confident", "romantic"],
                vibes=["synth", "upbeat", "anthem"],
                energy_preference="high"
            ),
            TasteZone(
                name="Chill Vibes",
                genres=["pop", "r&b", "indie pop"],
                moods=["dreamy", "romantic", "soft"],
                vibes=["mellow", "smooth", "atmospheric"],
                energy_preference="medium"
            ),
        ],
        listening_frequency="enthusiast"
    ),
    UserTasteProfile(
        id="indie_lover",
        name="Indie Vibes",
        top_genres=["indie", "alternative", "rock", "synth-pop"],
        top_artists=["Arctic Monkeys", "Tame Impala", "The 1975", "MGMT", "Beach House"],
        taste_zones=[
            TasteZone(
                name="Late Night Drive",
                genres=["indie", "synth-pop", "electronic"],
                moods=["dreamy", "nostalgic", "reflective"],
                vibes=["synth", "atmospheric", "retro"],
                energy_preference="medium"
            ),
            TasteZone(
                name="Live Energy",
                genres=["rock", "alternative", "indie rock"],
                moods=["energetic", "confident", "powerful"],
                vibes=["guitar-driven", "anthemic", "high-energy"],
                energy_preference="high"
            ),
        ],
        listening_frequency="regular"
    ),
    UserTasteProfile(
        id="hip_hop_head",
        name="Hip-Hop Head",
        top_genres=["hip-hop", "rap", "r&b", "trap"],
        top_artists=["Kendrick Lamar", "J. Cole", "Drake", "Travis Scott", "Tyler, the Creator"],
        taste_zones=[
            TasteZone(
                name="Grind Mode",
                genres=["hip-hop", "rap", "trap"],
                moods=["determined", "confident", "intense"],
                vibes=["bass", "hard-hitting", "lyrical"],
                energy_preference="high"
            ),
            TasteZone(
                name="Wind Down",
                genres=["r&b", "hip-hop", "soul"],
                moods=["reflective", "smooth", "romantic"],
                vibes=["mellow", "smooth", "groovy"],
                energy_preference="low"
            ),
        ],
        listening_frequency="enthusiast"
    ),
    UserTasteProfile(
        id="chill_listener",
        name="Chill Vibes",
        top_genres=["ambient", "lo-fi", "acoustic", "folk"],
        top_artists=["Bon Iver", "Mac DeMarco", "Khruangbin", "Tycho", "Nujabes"],
        taste_zones=[
            TasteZone(
                name="Focus Mode",
                genres=["ambient", "lo-fi", "instrumental"],
                moods=["calm", "peaceful", "focused"],
                vibes=["ambient", "minimal", "soothing"],
                energy_preference="low"
            ),
            TasteZone(
                name="Sunday Morning",
                genres=["acoustic", "folk", "indie folk"],
                moods=["warm", "nostalgic", "reflective"],
                vibes=["organic", "acoustic", "gentle"],
                energy_preference="low"
            ),
        ],
        listening_frequency="casual"
    ),
    UserTasteProfile(
        id="eclectic_mix",
        name="Eclectic Mix",
        top_genres=["electronic", "indie", "pop", "r&b", "rock"],
        top_artists=["Radiohead", "Björk", "James Blake", "The Weeknd", "Portishead"],
        taste_zones=[
            TasteZone(
                name="Experimental",
                genres=["electronic", "experimental", "art pop"],
                moods=["mysterious", "intense", "dreamy"],
                vibes=["atmospheric", "dark", "avant-garde"],
                energy_preference="medium"
            ),
            TasteZone(
                name="Sing-Along",
                genres=["pop", "indie rock", "alternative"],
                moods=["euphoric", "confident", "nostalgic"],
                vibes=["anthemic", "upbeat", "sing-along"],
                energy_preference="medium-high"
            ),
            TasteZone(
                name="Late Night",
                genres=["r&b", "electronic", "ambient"],
                moods=["romantic", "reflective", "soft"],
                vibes=["smooth", "mellow", "atmospheric"],
                energy_preference="low"
            ),
        ],
        listening_frequency="enthusiast"
    ),
]
