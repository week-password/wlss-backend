from __future__ import annotations

from pydantic import BaseModel

from src.health.enums import HealthStatus


class Health(BaseModel):
    status: HealthStatus
