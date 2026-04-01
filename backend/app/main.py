import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file explicitly
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import recommend

app = FastAPI(
    title="Soundtrack API",
    description="AI-powered contextual music recommendations",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api", tags=["recommendations"])


@app.get("/api/health")
def health_check():
    return {
        "status": "ok", 
        "message": "Soundtrack API is running",
        "groq_enabled": bool(os.getenv("GROQ_API_KEY"))
    }
