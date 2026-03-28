# Soundtrack - Contextual Music Recommendation App

AI-powered music recommendations based on your current situation.

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key (get from https://platform.openai.com/api-keys)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here

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
2. You should see the app with the input form
3. The backend health check: http://localhost:8000/api/health

## Tech Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python, SQLAlchemy
- **AI:** OpenAI GPT-4o-mini

## Project Structure

```
/frontend          - Next.js app
/backend           - FastAPI app
  /app/api         - API routes
  /app/services    - Business logic
  /app/schemas     - Request/response models
  /data            - Song catalog
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## MVP Features

- [ ] Natural language situation input
- [ ] AI-powered situation analysis
- [ ] Curated song catalog
- [ ] Recommendation ranking
- [ ] "Why this song" explanations
- [ ] Spotify links

## Next Steps (Phase 3)

1. Implement situation analyzer (LLM integration)
2. Build song catalog service
3. Create recommendation engine
4. Connect frontend to backend
5. Add loading states and error handling
