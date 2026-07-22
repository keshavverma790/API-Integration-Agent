from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Expose a simple liveness endpoint for local checks and deployment probes."""
    return "OK"
