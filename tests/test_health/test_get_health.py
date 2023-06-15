from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client"})
async def test_get_health_returns_correct_response(f):
    result = await f.client.get("/health")

    assert result.status_code == 200
    assert result.json() == {"status": "OK"}
