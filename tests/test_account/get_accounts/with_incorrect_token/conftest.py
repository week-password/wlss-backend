from __future__ import annotations

import jwt
import pytest

from src.config import CONFIG


@pytest.fixture
async def access_token_incorrect():
    payload = {
        "account_id": 1,
        # missing "created_at" field
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
