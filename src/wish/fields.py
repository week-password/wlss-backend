"""Field definitions for Pydantic models."""

from __future__ import annotations

from src.shared.fields import StrField


class Description(StrField):
    """Description value field."""

    FIELD_NAME = "Wish Description"
    LENGTH_MAX = 10000
    LENGTH_MIN = 1
    REGEXP = r".*"


class Title(StrField):
    """Name value field."""

    FIELD_NAME = "Profile Name"
    LENGTH_MAX = 100
    LENGTH_MIN = 1

    REGEXP = r"[A-Za-zА-яЁё'-.() ]*"  # noqa: RUF001
