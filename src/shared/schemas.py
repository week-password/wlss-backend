from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from api.shared.schemas import Schema


T = TypeVar("T", bound=BaseModel)


class HTTPError(Schema):
    """Base schema for errors."""

    description: str
    details: str


class NotAuthenticatedResponse(HTTPError):  # noqa: N818
    """Schema for 401 UNAUTHORIZED response."""


class NotFoundResponse(HTTPError):  # noqa: N818
    """Schema for 404 NOT FOUND error."""

    resource: str


class NotAllowedResponse(HTTPError):  # noqa: N818
    """Schema for 403 FORBIDDEN error."""

    action: str
