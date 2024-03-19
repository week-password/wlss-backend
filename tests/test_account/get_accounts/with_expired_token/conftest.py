from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
import pytest

from api.shared.datetime import DATETIME_FORMAT
from src.config import CONFIG


@pytest.fixture
async def access_token_expired():
    payload = {
        "account_id": 1,
        "created_at": (
            (
                datetime.now(tz=timezone.utc) - timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION + 1)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
