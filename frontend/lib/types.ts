export interface RecommendRequest {
  situation: string;
  genres?: string[];
  artists?: string[];
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
