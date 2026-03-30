# Soundtrack - Contextual Music Recommendation App

AI-powered music recommendations based on your current real-life situation.

> "Describe your moment, get the right soundtrack for it."

## The Problem

Existing music apps require you to think in genres or playlists. When you want music that matches a specific moment ("I'm nervous before a date"), you have no good way to find it.

## The Solution

This app understands your current situation — not just genre — and recommends songs that fit:
- The emotional/contextual meaning of your moment
- Your personal music taste

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Groq API key (get from https://console.groq.com/keys)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install Groq
pip install groq

# Set up environment variables
# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here

# Run the backend
uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

Frontend runs at: http://localhost:3000

### Verify Setup

1. Open http://localhost:3000 in your browser
2. Describe your current moment
3. Get personalized song recommendations

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python 3.11+ |
| **AI** | Groq (Llama 3.1) |
| **Storage** | JSON file-based song catalog |

## Project Structure

```
/frontend              - Next.js app
  /app
    page.tsx          - Main input page
    results/          - Recommendations display
    demo/             - Situation analyzer demo
  /lib                - API client, types

/backend               - FastAPI app
  /app
    /api/routes       - API endpoints
    /services         - Business logic
      situation_analyzer.py   - AI situation extraction
      recommender.py          - Song ranking engine
    /schemas          - Pydantic models
  /data
    songs.json        - Song catalog (100+ songs)
```

## Features

### Completed
- [x] Natural language situation input
- [x] AI-powered situation analysis (emotion, energy, setting, intent)
- [x] Curated song catalog (100+ songs with metadata)
- [x] Multi-dimensional taste profiles (multiple taste zones)
- [x] Recommendation ranking engine
- [x] "Why this song" explanations
- [x] Spotify deep links
- [x] Fallback mode (rule-based when no API key)

### How It Works

1. **You describe your moment** — "I'm in the metro going to meet my crush and I'm nervous but excited"

2. **AI extracts the situation** — analyzes emotions, energy level, setting, and intent

3. **Engine ranks songs** — combines situation match (70%) with taste match (30%)

4. **You get recommendations** — ranked songs with explanations and Spotify links

## Environment Variables

### Backend (.env)
```
# Groq API Key (required for AI features)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Change model (defaults to llama-3.1-70b-versatile)
GROQ_MODEL=llama-3.1-70b-versatile
```

### Fallback Mode

If no `GROQ_API_KEY` is set, the app uses rule-based fallback analysis. You'll see:
```
GROQ_API_KEY not set - using fallback mode
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recommend` | POST | Get song recommendations |
| `/api/analyze-situation` | POST | Analyze situation text |
| `/api/recommend/profiles` | GET | List mock taste profiles |
| `/api/health` | GET | Health check |

## Demo

Visit http://localhost:3000/demo to test the situation analyzer separately.

## Future Enhancements

- Spotify integration (connect account for real taste data)
- More songs in catalog
- AI-generated "why" explanations
- User accounts / history
- Mobile app

## License

MIT
