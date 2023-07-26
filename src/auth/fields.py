"""Field definitions for Pydantic models."""

from __future__ import annotations

from src.shared.fields import SecretStrField


class Password(SecretStrField):
    """Password value field."""

    FIELD_NAME = "Password"
    LENGTH_MIN = 8
    LENGTH_MAX = 500
