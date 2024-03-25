from __future__ import annotations

from fastapi import status

from src.shared.exceptions import BadRequestException, NotFoundException, TooLargeException


class FileAlreadyInUse(BadRequestException):
    action: str = "Use file"

    description = "Request is not correct."
    details = "Request contains file that is already in use in somewhere else."
    status_code = status.HTTP_400_BAD_REQUEST


class FileNotFoundError(NotFoundException):  # noqa: A001
    resource: str = "File"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class FileTooLarge(TooLargeException):
    """Exception raised when file user tries to upload is too large."""

    resource = "file"

    description = "File size is too large."
    details = "File size is too large and it cannot be handled."
