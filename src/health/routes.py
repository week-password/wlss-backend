"""Health endpoints."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def get_health() -> dict[str, str]:
    """Classic health check function."""
    return {"status": "OK"}
