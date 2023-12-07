"""Security stuff for auth related functionality."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.schemas import AccessTokenPayload, RefreshTokenPayload


def get_access_token(  # type: ignore[empty-body]
    token: Annotated[  # noqa: ARG001
        HTTPAuthorizationCredentials,
        Depends(
            HTTPBearer(
                scheme_name="Access token",
                description="Short-living token needed to authenticate the request.",
            ),
        ),
    ],
) -> AccessTokenPayload:
    """Get payload from decoded and verified access token. FastAPI dependency."""


def get_refresh_token(  # type: ignore[empty-body]
    token: Annotated[  # noqa: ARG001
        HTTPAuthorizationCredentials,
        Depends(
            HTTPBearer(
                scheme_name="Refresh token",
                description="Long-living token needed to refresh expired tokens.",
            ),
        ),
    ],
) -> RefreshTokenPayload:
    """Get payload from decoded and verified refresh token. FastAPI dependency."""
