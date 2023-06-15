from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_entity"})
async def test_get_entity_returns_200_with_correct_body(f):
    result = await f.client.get("/entities/1")

    assert result.status_code == 200
    assert result.json() == {"id": 1, "bucket": "entity", "key": "entity-key"}
