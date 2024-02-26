from __future__ import annotations

from fastapi import APIRouter, status

from src.health import enums, schemas


router = APIRouter(tags=["service"])


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
)
async def get_health() -> schemas.Health:
    return schemas.Health(status=enums.HealthStatus.OK)
