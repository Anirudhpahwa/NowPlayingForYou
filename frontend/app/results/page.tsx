"use client";

import { useEffect, useState } from "react";
import { RecommendationResult, RecommendResponse } from "@/lib/types";

export default function ResultsPage() {
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);
  const [situationAnalysis, setSituationAnalysis] = useState<any>(null);
  const [lastSituation, setLastSituation] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = sessionStorage.getItem("recommendations");
    const situation = sessionStorage.getItem("lastSituation");
    
    if (stored) {
      const data: RecommendResponse = JSON.parse(stored);
      setRecommendations(data.recommendations || []);
      setSituationAnalysis(data.situation_analysis);
    }
    if (situation) {
      setLastSituation(situation);
    }
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-12 h-12 border-4 border-slate-200 border-t-slate-900 rounded-full mx-auto mb-4"></div>
          <p className="text-slate-500">Finding your soundtrack...</p>
        </div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="text-center max-w-md">
          <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-slate-900 mb-2">No recommendations yet</h2>
          <p className="text-slate-500 mb-6">Go back and describe your moment to get started.</p>
          <a 
            href="/" 
            className="inline-flex items-center gap-2 px-6 py-3 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Describe your moment
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <div className="mb-8">
        <a 
          href="/" 
          className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 transition-colors mb-6"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Start over
        </a>

        <h1 className="text-3xl font-bold text-slate-900 mb-2">Your Soundtrack</h1>
        <p className="text-slate-500 mb-4">"{lastSituation}"</p>

        {/* Situation Analysis Tags */}
        {situationAnalysis && (
          <div className="flex flex-wrap gap-2 mb-6">
            {situationAnalysis.emotions?.map((emotion: string, i: number) => (
              <span key={`emotion-${i}`} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                {emotion}
              </span>
            ))}
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
              {situationAnalysis.energy}
            </span>
            {situationAnalysis.settings?.map((setting: string, i: number) => (
              <span key={`setting-${i}`} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                {setting}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Results List */}
      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div 
            key={rec.song.id} 
            className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-shadow p-6 border border-slate-100"
          >
            <div className="flex items-start gap-4">
              {/* Rank */}
              <div className="flex-shrink-0 w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center text-sm font-semibold text-slate-500">
                {index + 1}
              </div>

              {/* Song Info */}
              <div className="flex-grow min-w-0">
                <h3 className="font-semibold text-slate-900 text-lg truncate">{rec.song.title}</h3>
                <p className="text-slate-500 truncate">{rec.song.artist}</p>
                
                {/* Tags */}
                <div className="flex flex-wrap gap-1 mt-2">
                  {rec.song.moods.slice(0, 3).map((mood, i) => (
                    <span key={i} className="px-2 py-0.5 bg-slate-50 text-slate-500 rounded text-xs">
                      {mood}
                    </span>
                  ))}
                </div>

                {/* Why */}
                <p className="mt-3 text-sm text-slate-600 italic leading-relaxed">
                  "{rec.why}"
                </p>
              </div>

              {/* Spotify Button */}
              <div className="flex-shrink-0">
                <a
                  href={rec.song.spotify_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-full text-sm font-medium transition-colors"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                  </svg>
                  Play
                </a>
              </div>
            </div>

            {/* Score indicator */}
            <div className="mt-4 flex items-center gap-2">
              <div className="flex-grow h-1 bg-slate-100 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                  style={{ width: `${Math.min(rec.score, 100)}%` }}
                />
              </div>
              <span className="text-xs text-slate-400">{Math.round(rec.score)}% match</span>
            </div>
          </div>
        ))}
      </div>

      {/* Footer CTA */}
      <div className="mt-8 text-center">
        <a 
          href="/" 
          className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Try another moment
        </a>
      </div>
    </div>
  );
}
