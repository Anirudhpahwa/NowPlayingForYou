import json
import os
from typing import Optional

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

from app.schemas.situation import SituationProfile


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

VALID_ENERGY_LEVELS = ["low", "medium", "medium-high", "high"]


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


class SituationAnalyzer:
    """
    Uses Groq LLM to extract structured situation attributes from natural language.
    Falls back to rule-based analysis if Groq is unavailable.
    """
    
    def __init__(self):
        self.client: Optional[Groq] = None
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        self.use_groq = False
        
        # Try to initialize Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not set - using fallback mode")
            return
            
        if not GROQ_AVAILABLE:
            print("Groq library not installed - using fallback mode")
            return
            
        try:
            self.client = Groq(api_key=api_key)
            self.use_groq = True
            print(f"Using Groq with model: {self.model}")
        except Exception as e:
            print(f"Failed to initialize Groq: {e} - using fallback mode")
    
    def analyze(self, situation_text: str) -> SituationProfile:
        """
        Analyze user situation text and return structured profile.
        Uses Groq if available, otherwise falls back to rule-based analysis.
        """
        if self.use_groq and self.client:
            try:
                return self._analyze_with_groq(situation_text)
            except Exception as e:
                print(f"Groq analysis failed: {e} - falling back to rule-based")
        
        return self._fallback_analysis(situation_text)
    
    def _analyze_with_groq(self, situation_text: str) -> SituationProfile:
        """Use Groq API for situation analysis."""
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
    
    def _fallback_analysis(self, situation_text: str) -> SituationProfile:
        """
        Simple rule-based fallback if LLM is unavailable.
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
