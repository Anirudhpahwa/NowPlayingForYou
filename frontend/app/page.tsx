"use client";

import { useState, useEffect } from "react";
import { getTasteProfiles } from "@/lib/api";
import { UserTasteProfile } from "@/lib/types";

export default function Home() {
  const [situation, setSituation] = useState("");
  const [profiles, setProfiles] = useState<UserTasteProfile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    getTasteProfiles().then(setProfiles).catch(console.error);
  }, []);

  const handleSubmit = async () => {
    if (!situation.trim()) return;
    
    setIsLoading(true);
    
    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          situation,
          profile_id: selectedProfile || undefined,
        }),
      });
      
      const data = await response.json();
      
      // Store results and navigate
      sessionStorage.setItem("recommendations", JSON.stringify(data));
      sessionStorage.setItem("lastSituation", situation);
      window.location.href = "/results";
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <header className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-slate-900">Soundtrack</h1>
        <p className="text-lg text-slate-600">Describe your moment, get the right soundtrack.</p>
      </header>

      <div className="bg-white rounded-2xl shadow-lg p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            What's happening right now?
          </label>
          <textarea
            className="w-full h-32 p-4 border border-slate-200 rounded-xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., I'm in the metro going to meet my crush and I'm nervous but excited..."
            value={situation}
            onChange={(e) => setSituation(e.target.value)}
          />
        </div>

        <div className="pt-4 border-t border-slate-100">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-slate-500">
              Dev Mode: Select a mock taste profile
            </p>
            <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
              Temp
            </span>
          </div>
          <select
            className="w-full p-3 border border-slate-200 rounded-lg text-sm bg-white"
            value={selectedProfile}
            onChange={(e) => setSelectedProfile(e.target.value)}
          >
            <option value="">No profile (situation only)</option>
            {profiles.map((profile) => (
              <option key={profile.id} value={profile.id}>
                {profile.name} — {profile.top_genres.slice(0, 2).join(", ")}
              </option>
            ))}
          </select>
          {selectedProfile && (
            <div className="mt-2 p-3 bg-slate-50 rounded-lg text-xs text-slate-600">
              <p><strong>Genres:</strong> {profiles.find(p => p.id === selectedProfile)?.top_genres.join(", ")}</p>
              <p><strong>Artists:</strong> {profiles.find(p => p.id === selectedProfile)?.top_artists.join(", ")}</p>
              <p><strong>Energy:</strong> {profiles.find(p => p.id === selectedProfile)?.preferred_energy}</p>
            </div>
          )}
        </div>

        <button 
          onClick={handleSubmit}
          disabled={!situation.trim() || isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-colors"
        >
          {isLoading ? "Finding your soundtrack..." : "Get My Soundtrack"}
        </button>
      </div>

      <footer className="text-center text-sm text-slate-400">
        Powered by AI • Links to Spotify
      </footer>
    </div>
  );
}
