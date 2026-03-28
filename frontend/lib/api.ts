import { RecommendRequest, RecommendResponse } from "./types";

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
