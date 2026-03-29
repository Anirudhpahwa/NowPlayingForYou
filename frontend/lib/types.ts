export interface RecommendRequest {
  situation: string;
  profile_id?: string;
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
