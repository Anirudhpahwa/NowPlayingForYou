export default function Home() {
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
          />
        </div>

        <div className="pt-4 border-t border-slate-100">
          <p className="text-sm text-slate-500 mb-4">
            Optional: Tell us your music taste
          </p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-500 mb-1">Favorite genres</label>
              <input
                type="text"
                className="w-full p-2 border border-slate-200 rounded-lg text-sm"
                placeholder="pop, indie, rock..."
              />
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">Favorite artists</label>
              <input
                type="text"
                className="w-full p-2 border border-slate-200 rounded-lg text-sm"
                placeholder="The Weeknd, Arctic..."
              />
            </div>
          </div>
        </div>

        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-xl transition-colors">
          Get My Soundtrack
        </button>
      </div>

      <footer className="text-center text-sm text-slate-400">
        Powered by AI • Links to Spotify
      </footer>
    </div>
  );
}
