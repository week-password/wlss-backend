"""Schemas for file related functionality."""

from __future__ import annotations

from uuid import UUID

from src.file.enums import Extension, MimeType
from src.file.fields import Name, Size
from src.shared.schemas import Schema


class File(Schema):
    """File schema."""

    id: UUID  # noqa: A003

    extension: Extension
    mime_type: MimeType
    name: Name
    size: Size
