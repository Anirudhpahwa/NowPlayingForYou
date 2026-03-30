"use client";

import { useState } from "react";

const EXAMPLE_PROMPTS = [
  "I'm in the metro going to meet my crush and I'm nervous but excited",
  "I just finished a workout and I want to feel powerful",
  "It's 2am and I'm driving home on an empty highway",
  "I'm studying for exams and need music that helps me focus",
  "I'm getting ready for a night out with friends"
];

export default function Home() {
  const [situation, setSituation] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!situation.trim()) return;
    
    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ situation }),
      });
      
      if (!response.ok) {
        throw new Error("Failed to get recommendations");
      }
      
      const data = await response.json();
      sessionStorage.setItem("recommendations", JSON.stringify(data));
      sessionStorage.setItem("lastSituation", situation);
      window.location.href = "/results";
    } catch (e) {
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && e.metaKey && situation.trim()) {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-slate-900 mb-3 tracking-tight">
          Soundtrack
        </h1>
        <p className="text-xl text-slate-500 max-w-md mx-auto">
          Describe your moment. Get the perfect soundtrack.
        </p>
      </div>

      {/* Main Input Card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <label className="block text-sm font-medium text-slate-700 mb-3">
          What's happening right now?
        </label>
        
        <textarea
          className="w-full h-36 p-5 border-2 border-slate-100 rounded-xl resize-none text-lg focus:border-blue-400 focus:ring-0 transition-colors placeholder:text-slate-300"
          placeholder="Tell us about your moment..."
          value={situation}
          onChange={(e) => setSituation(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />

        {/* Example prompts */}
        {!situation && (
          <div className="mt-4">
            <p className="text-xs text-slate-400 mb-2 uppercase tracking-wider">Try describing:</p>
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_PROMPTS.map((prompt, i) => (
                <button
                  key={i}
                  onClick={() => setSituation(prompt)}
                  className="text-sm text-slate-500 bg-slate-50 hover:bg-blue-50 hover:text-blue-600 px-3 py-1.5 rounded-full transition-colors"
                >
                  {prompt.slice(0, 40)}...
                </button>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">
            {error}
          </div>
        )}

        <button 
          onClick={handleSubmit}
          disabled={!situation.trim() || isLoading}
          className="w-full mt-6 bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-xl transition-all transform hover:scale-[1.01] active:scale-[0.99] text-lg"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Finding your soundtrack...
            </span>
          ) : (
            "Find My Soundtrack"
          )}
        </button>

        <p className="text-center text-xs text-slate-400 mt-4">
          Press Cmd+Enter to submit
        </p>
      </div>

      {/* Features */}
      <div className="grid grid-cols-3 gap-6 text-center">
        <div>
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <p className="text-sm font-medium text-slate-700">Describe your moment</p>
          <p className="text-xs text-slate-400 mt-1">In your own words</p>
        </div>
        <div>
          <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p className="text-sm font-medium text-slate-700">AI understands context</p>
          <p className="text-xs text-slate-400 mt-1">Emotion, energy, setting</p>
        </div>
        <div>
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
          </div>
          <p className="text-sm font-medium text-slate-700">Get personalized songs</p>
          <p className="text-xs text-slate-400 mt-1">Curated for your moment</p>
        </div>
      </div>

      <footer className="mt-auto pt-12 text-center text-sm text-slate-400">
        <p>Links to Spotify • Free to use</p>
      </footer>
    </div>
  );
}
