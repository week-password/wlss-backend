"""File for high level pytest fixtures."""

from __future__ import annotations

import asyncio

import pytest
from alembic.config import main as alembic
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, AsyncSession, create_async_engine

from src.app import app
from src.shared.database import get_session, POSTGRES_CONNECTION_URL
from tests.utils.database import set_autoincrement_counters


def pytest_sessionstart(session: AsyncSession):
    """Pytest initialization hook.

    Called after the Session object has been created and before performing collection and entering the run test loop.

    :param session: The pytest session object.
    """
    alembic(["upgrade", "head"])
    set_autoincrement_counters()


@pytest.fixture
def anyio_backend():
    """Choose anyio back-end runner as asyncio. Source https://anyio.readthedocs.io/en/1.4.0/testing.html."""
    return "asyncio"


@pytest.fixture
async def client(db):
    """Async client."""
    def override_get_session():
        yield db
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://") as async_client:
        yield async_client


@pytest.fixture
async def db():
    """Empty database session."""
    # this solution is from sqlalchemy docs:
    # https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    async_engine = create_async_engine(POSTGRES_CONNECTION_URL)
    connection = await async_engine.connect()
    transaction = await connection.begin()
    async_session = async_scoped_session(async_sessionmaker(bind=connection), scopefunc=asyncio.current_task)

    yield async_session

    await async_session.close()
    await transaction.rollback()
    await connection.close()
