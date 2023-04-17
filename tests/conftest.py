"""File for high level pytest fixtures."""

import pytest
from httpx import AsyncClient

from src.app import app


@pytest.fixture
def anyio_backend():
    """Choose anyio back-end runner as asyncio. Source https://anyio.readthedocs.io/en/1.4.0/testing.html."""
    return "asyncio"


@pytest.fixture
async def client():
    """Async client."""
    async with AsyncClient(app=app, base_url="http://") as async_client:
        yield async_client
