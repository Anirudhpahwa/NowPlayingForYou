import { RecommendRequest, RecommendResponse, ProfileListResponse, UserTasteProfile } from "./types";

const API_BASE = "/api";

export async function getRecommendations(
  request: RecommendRequest
): Promise<RecommendResponse> {
  const response = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function getTasteProfiles(): Promise<UserTasteProfile[]> {
  const response = await fetch(`${API_BASE}/recommend/profiles`);
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  
  const data: ProfileListResponse = await response.json();
  return data.profiles;
}
