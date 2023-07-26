"""Exceptions for auth related functionality."""

from __future__ import annotations

from src.shared.exceptions import HTTPException


class NotAuthenticatedException(HTTPException):
    """Exception for 401 UNAUTHORIZED error."""

    description = "Request initiator is not authenticated."
    details = "Your credentials or tokens are invalid or missing."
