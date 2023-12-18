"""Exceptions related to file functionality."""

from __future__ import annotations

from src.shared.exceptions import TooLargeException


class FileTooLarge(TooLargeException):
    """Exception raised when file user tries to upload is too large."""

    resource = "file"

    description = "File size is too large."
    details = "File size is too large and it cannot be handled."
