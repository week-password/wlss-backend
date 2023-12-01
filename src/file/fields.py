"""Field definitions for Pydantic models."""

from __future__ import annotations

from src.file.constants import BYTE, MEGABYTE
from src.shared.fields import IntField


class Size(IntField):
    """File size value field."""

    FIELD_NAME = "File size in bytes"
    VALUE_MAX = 10 * MEGABYTE
    VALUE_MIN = 1 * BYTE
