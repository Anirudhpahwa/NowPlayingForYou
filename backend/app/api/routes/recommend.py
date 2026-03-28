from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Soundtrack API is running. Use POST /api/recommend for recommendations."}
