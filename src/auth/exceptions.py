from __future__ import annotations

from fastapi import status

from src.shared.exceptions import NotAllowedException, NotAuthenticatedException, NotFoundException


class CannotAuthorizeError(NotAllowedException):
    action: str = "Authorization"

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotDeleteSessionError(NotAllowedException):
    action: str = "Delete session"

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotDeleteAllSessionsError(NotAllowedException):
    action: str = "Delete all sessions"

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotRefreshTokensError(NotAllowedException):
    action: str = "Refresh tokens"

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class InvalidCredentialsError(NotAuthenticatedException):
    description = "Request initiator is not authenticated."
    details = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class SessionNotFoundError(NotFoundException):
    resource: str = "Session"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class TokenExpiredError(NotAllowedException):
    action = "Token validation"

    description = "Token expired."
    details = "Provided token is expired."
    status_code = status.HTTP_403_FORBIDDEN
