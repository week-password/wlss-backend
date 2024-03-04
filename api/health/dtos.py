from __future__ import annotations

from api.shared.schemas import Schema
from src.health.enums import HealthStatus


class HealthResponse(Schema):
    status: HealthStatus
