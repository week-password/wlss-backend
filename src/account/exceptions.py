"""Exceptions related to account functionality."""

from __future__ import annotations

from src.shared.exceptions import BadRequestException


class DuplicateAccountException(BadRequestException):
    """Exception raised when such account already exists."""

    action = "create account"

    description = "Account already exists."
    details: str = "There is another account with same value for one of the unique fields."
