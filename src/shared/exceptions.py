"""Exceptions shared by different application components."""

from __future__ import annotations

from fastapi import status


class HTTPException(Exception):  # noqa: N818
    """Base class for all app exceptions."""

    description = "Unknown error occured."
    details = "Please contact backend maintenance team."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NotAuthenticatedException(HTTPException):
    """Exception for 401 UNAUTHORIZED error."""

    description = "Request initiator is not authenticated."
    details = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class NotFoundException(HTTPException):
    """Exception for 404 NOT FOUND error."""

    resource: str

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class NotAllowedException(HTTPException):
    """Exception for 403 FORBIDDEN error."""

    action: str

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN
