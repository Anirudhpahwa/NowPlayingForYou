# Soundtrack

> AI-powered contextual music recommendations — describe your moment, get the perfect soundtrack.

A full-stack AI application that recommends songs based on your current real-life situation, mood, and intent — not just genres or algorithms.

---

## Demo

**Local:**
```bash
# Terminal 1 - Backend
cd backend && python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open http://localhost:3000
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **AI Situation Analysis** | Extracts emotion, energy, setting, and intent from natural language using Groq (Llama 3.1) |
| **Smart Recommendation Engine** | Combines situation match (70%) with user taste (30%) for personalized results |
| **Multi-dimensional User Profiles** | Supports multiple "taste zones" — reflecting how users enjoy different music in different contexts |
| **Fallback Mode** | Works without API key using rule-based analysis |
| **Spotify Integration** | One-click links to play recommended songs |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| **Backend** | FastAPI (Python), Pydantic |
| **AI** | Groq API (Llama 3.1-8b-instant) |
| **Data** | JSON song catalog with rich metadata |

---

## Architecture

```
User Input ("I'm nervous about my date")
         |
         v
+------------------------------------------+
|  Frontend (Next.js)                     |
|  - SituationInput component              |
|  - Results display with Spotify links    |
+---------------+--------------------------+
                 | HTTP POST /api/recommend
                 v
+------------------------------------------+
|  Backend (FastAPI)                      |
|                                          |
|  +----------------------------------+   |
|  | Situation Analyzer (Groq)        |   |
|  | - Extracts emotions              |   |
|  | - Classifies energy level        |   |
|  | - Identifies setting & intent    |   |
|  +----------------------------------+   |
|                 |                       |
|                 v                       |
|  +----------------------------------+   |
|  | Recommendation Engine            |   |
|  | - Filter by energy compatibility |   |
|  | - Score situation match (70%)   |   |
|  | - Score taste match (30%)        |   |
|  | - Rank and return top songs      |   |
|  +----------------------------------+   |
+------------------------------------------+
                 |
                 v
          Ranked Recommendations
          + "Why this song" explanations
```

---

## Project Structure

```
/frontend                         # Next.js 14 application
  /app
    /page.tsx                 # Main input screen
    /results/page.tsx        # Recommendations display
    /demo/page.tsx           # Situation analyzer demo
  /lib
    /api.ts                  # API client
    /types.ts                # TypeScript interfaces

/backend                          # FastAPI application
  /app
    /api/routes
      /recommend.py          # API endpoints
    /services
      /situation_analyzer.py # LLM-based situation extraction
      /recommender.py        # Song ranking logic
    /schemas
      /profile.py            # User taste profile models
      /situation.py          # Situation profile models
      /response.py           # API response models
    /main.py                 # FastAPI app entry point
  /data
    /songs.json              # Song catalog (100+ songs)
  /.env                      # Environment variables
```

---

## Configuration

Create `backend/.env`:
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

> **Note:** The app works without a Groq key using rule-based fallback mode.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recommend` | POST | Get song recommendations |
| `/api/analyze-situation` | POST | Analyze situation text |
| `/api/recommend/profiles` | GET | List mock taste profiles |
| `/api/health` | GET | Health check |

---

## What I Learned

- Building a full-stack app with **Next.js + FastAPI**
- Integrating **LLM APIs** (Groq) for natural language understanding
- Designing a **recommendation scoring algorithm** with weighted factors
- Creating **fallback systems** for graceful degradation
- Implementing **multi-dimensional user profiles** for better personalization

---

## Future Enhancements

- Spotify API integration for real user data
- Expand song catalog
- AI-generated "why" explanations
- User authentication & history

---

## License

MIT
