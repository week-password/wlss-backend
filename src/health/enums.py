from __future__ import annotations

from src.shared import enum


@enum.unique
@enum.types(str)
class HealthStatus(enum.Enum):
    """Possible health statuses."""

    OK = "OK"
