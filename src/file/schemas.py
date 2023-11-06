"""Schemas for file related functionality."""

from __future__ import annotations

from uuid import UUID

from src.shared.schemas import Schema


class File(Schema):
    """File schema."""

    id: UUID  # noqa: A003
