export interface RecommendRequest {
  situation: string;
  profile_id?: string;
}

export type EnergyLevel = "low" | "medium" | "medium-high" | "high";

export interface SituationProfile {
  raw_text: string;
  emotions: string[];
  energy: EnergyLevel;
  settings: string[];
  intents: string[];
}

export interface AnalyzeSituationRequest {
  situation: string;
}

export interface AnalyzeSituationResponse {
  situation_profile: SituationProfile;
}

export interface TasteZone {
  name: string;
  genres: string[];
  moods: string[];
  vibes: string[];
  energy_preference: string;
}

export interface UserTasteProfile {
  id: string;
  name: string;
  top_genres: string[];
  top_artists: string[];
  taste_zones: TasteZone[];
  listening_frequency: string;
}

export interface ProfileListResponse {
  profiles: UserTasteProfile[];
}

export interface Song {
  id: string;
  title: string;
  artist: string;
  genres: string[];
  moods: string[];
  energy: string;
  spotify_url: string;
  situations?: string[];
  vibes?: string[];
}

export interface RecommendationResult {
  song: Song;
  score: number;
  why: string;
}

export interface RecommendResponse {
  recommendations: RecommendationResult[];
  situation_analysis?: {
    emotions: string[];
    energy: string;
    setting: string;
    intent: string;
  };
}
