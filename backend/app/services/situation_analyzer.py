import json
import os
from openai import OpenAI

from app.schemas.situation import SituationProfile
from app.schemas.profile import EnergyLevel


VALID_EMOTIONS = [
    "nervous", "excited", "happy", "sad", "anxious", "confident",
    "reflective", "melancholic", "romantic", "powerful", "calm",
    "bored", "hopeful", "grateful", "energetic"
]

VALID_SETTINGS = [
    "transit", "commute", "workout", "gym", "walking", "driving",
    "night", "morning", "home", "office", "party", "date",
    "alone time", "exercise", "travel"
]

VALID_INTENTS = [
    "comfort", "motivation", "energy", "focus", "relaxation",
    "celebration", "reflection", "romance", "excitement", "calm"
]


SYSTEM_PROMPT = """You are a music situation analyzer. Given a user's description 
of their current moment, extract structured attributes.

Return ONLY valid JSON - no markdown, no explanation.

Valid emotions: nervous, excited, happy, sad, anxious, confident, reflective, melancholic, romantic, powerful, calm, bored, hopeful, grateful, energetic

Valid energy levels: low (calm/slow), medium (moderate), medium-high (upbeat), high (intense/fast)

Valid settings: transit, commute, workout, gym, walking, driving, night, morning, home, office, party, date, alone time, exercise, travel

Valid intents: comfort, motivation, energy, focus, relaxation, celebration, reflection, romance, excitement, calm

Output format:
{"emotions": [...], "energy": "...", "settings": [...], "intents": [...]}"""


USER_PROMPT_TEMPLATE = """Input: "{situation}"

Output:"""


def validate_and_normalize(
    emotions: list[str],
    energy: str,
    settings: list[str],
    intents: list[str]
) -> dict:
    """Validate and normalize extracted values to known tags."""
    normalized_emotions = [e.lower().strip() for e in emotions if e.lower().strip() in VALID_EMOTIONS]
    normalized_settings = [s.lower().strip() for s in settings if s.lower().strip() in VALID_SETTINGS]
    normalized_intents = [i.lower().strip() for i in intents if i.lower().strip() in VALID_INTENTS]
    
    if energy not in VALID_ENERGY_LEVELS:
        energy = "medium"
    
    return {
        "emotions": normalized_emotions,
        "energy": energy,
        "settings": normalized_settings,
        "intents": normalized_intents
    }


VALID_ENERGY_LEVELS = ["low", "medium", "medium-high", "high"]


class SituationAnalyzer:
    """
    Uses LLM to extract structured situation attributes from natural language.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def analyze(self, situation_text: str) -> SituationProfile:
        """
        Analyze user situation text and return structured profile.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT_TEMPLATE.format(situation=situation_text)}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            parsed = json.loads(content)
            
            normalized = validate_and_normalize(
                emotions=parsed.get("emotions", []),
                energy=parsed.get("energy", "medium"),
                settings=parsed.get("settings", []),
                intents=parsed.get("intents", [])
            )
            
            return SituationProfile(
                raw_text=situation_text,
                emotions=normalized["emotions"],
                energy=normalized["energy"],
                settings=normalized["settings"],
                intents=normalized["intents"]
            )
            
        except Exception as e:
            print(f"Situation analysis error: {e}")
            return self._fallback_analysis(situation_text)
    
    def _fallback_analysis(self, situation_text: str) -> SituationProfile:
        """
        Simple fallback if LLM fails.
        """
        text_lower = situation_text.lower()
        
        emotions = []
        if any(w in text_lower for w in ["nervous", "anxious", "worried"]):
            emotions.append("nervous")
        if any(w in text_lower for w in ["excited", "happy", "thrilled"]):
            emotions.append("excited")
        if any(w in text_lower for w in ["sad", "depressed", "down"]):
            emotions.append("sad")
        if any(w in text_lower for w in ["calm", "relaxed", "chill"]):
            emotions.append("calm")
        if any(w in text_lower for w in ["powerful", "strong", "confident"]):
            emotions.append("confident")
        
        settings = []
        if any(w in text_lower for w in ["metro", "train", "bus", "transit", "commute"]):
            settings.append("transit")
        if any(w in text_lower for w in ["gym", "workout", "exercise", "running"]):
            settings.append("workout")
        if any(w in text_lower for w in ["walking", "walk"]):
            settings.append("walking")
        if any(w in text_lower for w in ["driving", "car"]):
            settings.append("driving")
        if any(w in text_lower for w in ["night", "evening"]):
            settings.append("night")
        if any(w in text_lower for w in ["morning", "breakfast"]):
            settings.append("morning")
        
        energy = "medium"
        if any(w in text_lower for w in ["workout", "gym", "running", "intense", "powerful"]):
            energy = "high"
        elif any(w in text_lower for w in ["calm", "relaxing", "sleep", "resting"]):
            energy = "low"
        
        intents = []
        if any(w in text_lower for w in ["want", "need", "looking for"]):
            if any(w in text_lower for w in ["calm", "relax"]):
                intents.append("relaxation")
            if any(w in text_lower for w in ["energy", "power"]):
                intents.append("energy")
            if any(w in text_lower for w in ["motivate", "motivation"]):
                intents.append("motivation")
        
        return SituationProfile(
            raw_text=situation_text,
            emotions=emotions if emotions else ["neutral"],
            energy=energy,
            settings=settings,
            intents=intents
        )
