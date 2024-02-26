from __future__ import annotations

from fastapi import status

from src.shared.exceptions import BadRequestException, NotFoundException


class AccountNotFoundError(NotFoundException):
    resource: str = "Account"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class DuplicateAccountException(BadRequestException):
    action = "create account"

    description = "Account already exists."
    details: str = "There is another account with same value for one of the unique fields."
