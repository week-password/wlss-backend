"""Types shared across application modules."""

from __future__ import annotations

from api.shared.enum import Enum


class UrlSchema(Enum):
    """Enum class for URL schemas."""

    HTTP = "HTTP"
    HTTPS = "HTTPS"
