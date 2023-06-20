"""Health endpoints."""

from __future__ import annotations

from fastapi import APIRouter, status

from src.health import enums, schemas


router = APIRouter()


@router.get(
    "/health",
    description="Check backend health.",
    responses={
        status.HTTP_200_OK: {
            "description": "Backend application works fine.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "OK",
                    },
                },
            },
        },
    },
    response_model=schemas.Health,
    status_code=status.HTTP_200_OK,
    summary="Check health.",
    tags=["service"],
)
async def get_health() -> schemas.Health:
    """Classic health check function."""
    return schemas.Health(status=enums.HealthStatus.OK)
