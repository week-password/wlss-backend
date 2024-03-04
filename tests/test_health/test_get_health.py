from __future__ import annotations

import pytest

from api.health.dtos import HealthResponse
from src.health.enums import HealthStatus


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api"})
async def test_get_health_returns_correct_response(f):
    result = await f.api.health.get_health()

    assert isinstance(result, HealthResponse)
    assert result.model_dump() == {"status": HealthStatus.OK}
