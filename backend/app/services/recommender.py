import json
import os
from pathlib import Path
from typing import Optional

from app.schemas.situation import SituationProfile
from app.schemas.profile import UserTasteProfile
from app.schemas.response import Song


SONG_CATALOG_PATH = Path(__file__).parent.parent / "data" / "songs.json"

# Load songs at startup
_songs_cache: list[Song] | None = None


def load_songs() -> list[Song]:
    global _songs_cache
    if _songs_cache is None:
        with open(SONG_CATALOG_PATH, "r") as f:
            data = json.load(f)
            _songs_cache = [Song(**song) for song in data]
    return _songs_cache


def get_all_songs() -> list[Song]:
    return load_songs()


ENERGY_LEVELS = ["low", "medium", "medium-high", "high"]


def get_energy_distance(song_energy: str, target_energy: str) -> int:
    """Returns absolute distance between energy levels."""
    if song_energy not in ENERGY_LEVELS or target_energy not in ENERGY_LEVELS:
        return 2
    return abs(ENERGY_LEVELS.index(song_energy) - ENERGY_LEVELS.index(target_energy))


def score_song(
    song: Song,
    situation: SituationProfile,
    taste: Optional[UserTasteProfile] = None
) -> dict:
    """
    Score a single song based on situation and taste.
    Returns dict with breakdown of scores.
    """
    situation_score = 0.0
    taste_score = 0.0
    
    # === SITUATION SCORING (70%) ===
    
    # Emotion match (35%)
    emotion_matches = len(set(song.moods) & set(situation.emotions))
    emotion_score = min(emotion_matches / max(len(situation.emotions), 1), 1.0) * 35
    situation_score += emotion_score
    
    # Setting match (20%)
    setting_matches = len(set(song.situations or []) & set(situation.settings))
    setting_score = min(setting_matches / max(len(situation.settings), 1), 1.0) * 20
    situation_score += setting_score
    
    # Intent match (15%)
    # Map intents to relevant moods
    intent_to_mood = {
        "comfort": ["calm", "peaceful"],
        "relaxation": ["calm", "peaceful"],
        "calm": ["calm", "peaceful"],
        "motivation": ["powerful", "determined", "energetic"],
        "energy": ["energetic", "powerful"],
        "focus": ["calm", "reflective"],
        "reflection": ["reflective", "melancholic", "nostalgic"],
        "celebration": ["euphoric", "happy", "energetic"],
        "romance": ["romantic", "soft", "dreamy"],
        "excitement": ["euphoric", "energetic", "excited"]
    }
    
    intent_moods = set()
    for intent in situation.intents:
        if intent in intent_to_mood:
            intent_moods.update(intent_to_mood[intent])
    
    intent_matches = len(set(song.moods) & intent_moods)
    intent_score = min(intent_matches / max(len(situation.intents), 1), 1.0) * 15
    situation_score += intent_score
    
    # Energy match bonus (10%)
    energy_dist = get_energy_distance(song.energy, situation.energy)
    if energy_dist == 0:
        energy_bonus = 10
    elif energy_dist == 1:
        energy_bonus = 5
    else:
        energy_bonus = 0
    situation_score += energy_bonus
    
    # === TASTE SCORING (30%) ===
    
    if taste:
        # Genre match (15%)
        taste_genres = set(taste.top_genres)
        genre_matches = len(set(song.genres) & taste_genres)
        genre_score = min(genre_matches / max(len(taste.top_genres), 1), 1.0) * 15
        taste_score += genre_score
        
        # Artist match (10%)
        taste_artists = set(a.lower() for a in taste.top_artists)
        song_artist = song.artist.lower()
        artist_score = 10 if any(ta in song_artist for ta in taste_artists) else 0
        taste_score += artist_score
        
        # Vibe match from taste zones (5%)
        all_taste_vibes = set()
        all_taste_moods = set()
        all_taste_genres = set()
        for zone in taste.taste_zones:
            all_taste_vibes.update(zone.vibes)
            all_taste_moods.update(zone.moods)
            all_taste_genres.update(zone.genres)
        
        vibe_matches = len(set(song.vibe_tags or []) & all_taste_vibes)
        mood_matches = len(set(song.moods) & all_taste_moods)
        vibe_score = ((vibe_matches + mood_matches) / 10) * 5
        taste_score += min(vibe_score, 5)
    
    # Calculate final score
    final_score = (situation_score * 0.7) + (taste_score * 0.3)
    
    return {
        "final_score": round(final_score, 2),
        "situation_score": round(situation_score, 2),
        "taste_score": round(taste_score, 2),
        "emotion_matches": emotion_matches,
        "setting_matches": setting_matches,
        "energy_match": energy_dist == 0,
    }


def recommend(
    situation: SituationProfile,
    taste: Optional[UserTasteProfile] = None,
    limit: int = 8
) -> list[dict]:
    """
    Generate song recommendations based on situation and optional taste.
    """
    songs = load_songs()
    
    # Filter: remove songs with energy too far from situation
    filtered_songs = [
        s for s in songs
        if get_energy_distance(s.energy, situation.energy) <= 1
    ]
    
    # Score all filtered songs
    scored_songs = []
    for song in filtered_songs:
        scores = score_song(song, situation, taste)
        scored_songs.append({
            "song": song,
            "score": scores["final_score"],
            "score_breakdown": scores
        })
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top N
    return scored_songs[:limit]
