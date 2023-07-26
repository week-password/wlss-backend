"""Exceptions shared by different application components."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any, Self


class HTTPException(Exception):  # noqa: N818
    """Base class for all app exceptions."""

    description = "Unknown error occured."
    details = "Please contact backend maintenance team."

    def __init__(self: Self, details: str = "") -> None:  # pragma: no cover
        """Initialize object."""
        self.details = details
        super().__init__()


class NotFoundException(HTTPException):
    """Exception for 404 NOT FOUND error."""

    resource: str

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."

    def __init__(self: Self, resource: str, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        """Initialize object."""
        self.resource = resource
        super().__init__(*args, **kwargs)


class NotAllowedException(HTTPException):
    """Exception for 403 FORBIDDEN error."""

    action: str

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."

    def __init__(self: Self, action: str, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        """Initialize object."""
        self.action = action
        super().__init__(*args, **kwargs)
