from __future__ import annotations

import httpx
import pytest

from api.auth.dtos import CreateSessionRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.create_session(
            request_data=CreateSessionRequest.model_validate({"login": "john_doe", "password": "wrong password"}),
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
