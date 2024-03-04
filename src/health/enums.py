from __future__ import annotations

from api.shared import enum


@enum.unique
@enum.types(str)
class HealthStatus(enum.Enum):
    """Possible health statuses."""

    OK = "OK"
