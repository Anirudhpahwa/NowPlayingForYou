export interface RecommendRequest {
  situation: string;
  profile_id?: string;
}

export interface UserTasteProfile {
  id: string;
  name: string;
  top_genres: string[];
  top_artists: string[];
  preferred_energy: string;
  preferred_mood: string[];
  listening_frequency: string;
  preferred_vibes: string[];
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
