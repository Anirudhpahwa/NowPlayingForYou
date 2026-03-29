"use client";

import { useEffect, useState } from "react";
import { RecommendationResult } from "@/lib/types";

export default function ResultsPage() {
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);
  const [lastSituation, setLastSituation] = useState("");

  useEffect(() => {
    const stored = sessionStorage.getItem("recommendations");
    const situation = sessionStorage.getItem("lastSituation");
    
    if (stored) {
      const data = JSON.parse(stored);
      setRecommendations(data.recommendations || []);
    }
    if (situation) {
      setLastSituation(situation);
    }
  }, []);

  if (recommendations.length === 0) {
    return (
      <div className="space-y-6">
        <header>
          <a href="/" className="text-blue-600 hover:underline text-sm">
            ← Back to input
          </a>
        </header>
        <div className="bg-white rounded-2xl shadow-lg p-6 text-center">
          <p className="text-slate-600">No recommendations yet. Go back and describe your moment.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <header>
        <a href="/" className="text-blue-600 hover:underline text-sm">
          ← Back to input
        </a>
      </header>

      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Your Soundtrack</h2>
        <p className="text-slate-600 mb-6">
          Based on: "{lastSituation}"
        </p>

        <div className="space-y-4">
          {recommendations.map((rec, index) => (
            <div key={rec.song.id} className="border border-slate-100 rounded-xl p-4">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs text-slate-400 mr-2">#{index + 1}</span>
                  <h3 className="font-semibold text-slate-900 inline">{rec.song.title}</h3>
                  <p className="text-sm text-slate-500">{rec.song.artist}</p>
                </div>
                <a
                  href={rec.song.spotify_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-500 text-sm hover:underline"
                >
                  Listen on Spotify →
                </a>
              </div>
              <p className="mt-2 text-sm text-slate-600 italic">
                "{rec.why}"
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
