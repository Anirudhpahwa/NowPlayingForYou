"use client";

import { useState } from "react";
import { analyzeSituation } from "@/lib/api";
import { SituationProfile } from "@/lib/types";

export default function SituationAnalyzerDemo() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<SituationProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const examples = [
    "I'm in the metro going to meet my crush and I'm nervous but excited.",
    "I just finished a workout and I want to feel powerful.",
    "I'm walking home at night and I want something calm but not depressing.",
    "I'm studying for exams and need focus music.",
    "It's Saturday morning and I'm making breakfast."
  ];

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    setError("");
    setResult(null);
    
    try {
      const profile = await analyzeSituation(input);
      setResult(profile);
    } catch (e: any) {
      setError(e.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-bold">Situation Analyzer Demo</h1>
        <p className="text-slate-600">Test the AI situation understanding</p>
      </header>

      <div className="bg-white rounded-xl shadow p-4 space-y-4">
        <textarea
          className="w-full h-24 p-3 border border-slate-200 rounded-lg text-sm"
          placeholder="Describe your current situation..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <div className="flex flex-wrap gap-2">
          {examples.map((ex, i) => (
            <button
              key={i}
              onClick={() => setInput(ex)}
              className="text-xs bg-slate-100 hover:bg-slate-200 px-2 py-1 rounded"
            >
              Example {i + 1}
            </button>
          ))}
        </div>

        <button
          onClick={handleAnalyze}
          disabled={!input.trim() || loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white py-2 rounded-lg"
        >
          {loading ? "Analyzing..." : "Analyze Situation"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white rounded-xl shadow p-4 space-y-3">
          <h2 className="font-semibold">Extracted Profile:</h2>
          
          <div>
            <span className="text-sm font-medium text-slate-500">Emotions:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {result.emotions.map((e, i) => (
                <span key={i} className="bg-purple-100 text-purple-700 px-2 py-0.5 rounded text-sm">
                  {e}
                </span>
              ))}
            </div>
          </div>

          <div>
            <span className="text-sm font-medium text-slate-500">Energy:</span>
            <span className="ml-2 bg-green-100 text-green-700 px-2 py-0.5 rounded text-sm">
              {result.energy}
            </span>
          </div>

          <div>
            <span className="text-sm font-medium text-slate-500">Settings:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {result.settings.map((s, i) => (
                <span key={i} className="bg-blue-100 text-blue-700 px-2 py-0.5 rounded text-sm">
                  {s}
                </span>
              ))}
            </div>
          </div>

          <div>
            <span className="text-sm font-medium text-slate-500">Intents:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {result.intents.map((i, idx) => (
                <span key={idx} className="bg-orange-100 text-orange-700 px-2 py-0.5 rounded text-sm">
                  {i}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
