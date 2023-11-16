"""Pydantic models shared by different application components."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.shared.datetime import DATETIME_FORMAT


class Schema(BaseModel):
    """Customized 'BaseModel' class from pydantic."""

    class Config:
        """Pydantic's special class to configure pydantic models."""

        json_encoders = {datetime: lambda v: v.strftime(DATETIME_FORMAT)}


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
