"""Field definitions for Pydantic models."""

from __future__ import annotations

from src.shared.fields import StrField


class Email(StrField):
    """Email value field."""

    FIELD_NAME = "Email"
    LENGTH_MAX = 200
    LENGTH_MIN = 5
    REGEXP = r".+@.+\..+"


class Login(StrField):
    """Login value field."""

    FIELD_NAME = "Login"
    LENGTH_MAX = 50
    LENGTH_MIN = 1
    REGEXP = r"[A-Za-z0-9\-_]*"