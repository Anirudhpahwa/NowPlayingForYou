export default function ResultsPage() {
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
          Based on: "I'm in the metro going to meet my crush..."
        </p>

        <div className="space-y-4">
          {/* Placeholder results */}
          {[1, 2, 3].map((i) => (
            <div key={i} className="border border-slate-100 rounded-xl p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-slate-900">Song Title</h3>
                  <p className="text-sm text-slate-500">Artist Name</p>
                </div>
                <a
                  href="#"
                  className="text-green-500 text-sm hover:underline"
                >
                  Listen on Spotify →
                </a>
              </div>
              <p className="mt-2 text-sm text-slate-600 italic">
                "Why this song was recommended..."
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
