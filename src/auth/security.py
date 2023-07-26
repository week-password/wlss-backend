"""Security stuff for auth related functionality."""

from __future__ import annotations

from fastapi.security import HTTPBearer


get_token = HTTPBearer(
    scheme_name="Access Token",
    description="Short-living token needed to authenticate the request.",
)
