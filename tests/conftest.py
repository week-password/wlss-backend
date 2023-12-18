"""File for high level pytest fixtures."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine

from src.app import app
from src.shared.database import get_session, POSTGRES_CONNECTION_URL
from src.shared.minio import get_minio
from tests.utils.database import set_autoincrement_counters


@pytest.fixture(scope="session", autouse=True)
def _initialize_db():
    """Prepare database before test run."""
    set_autoincrement_counters()


@pytest.fixture
def anyio_backend():
    """Choose anyio back-end runner as asyncio. Source https://anyio.readthedocs.io/en/1.4.0/testing.html."""
    return "asyncio"


@pytest.fixture
async def client(db_empty):
    """Async client."""
    def override_get_session():
        yield db_empty
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://") as async_client:
        yield async_client


@pytest.fixture
async def db_empty():
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


@pytest.fixture
async def minio_empty():
    """Empty minio."""
    minio = next(get_minio())
    for _, bucket_name in minio.BUCKETS:
        for minio_object in minio.list_objects(bucket_name, recursive=True):
            minio.remove_object(bucket_name, minio_object.object_name)
    return minio


@pytest.fixture
def f(request):
    """Load fixtures declared via 'fixtures' mark and put it into 'f' as its attributes."""
    fixtures = SimpleNamespace()
    marker = request.node.get_closest_marker("fixtures")
    if not marker:
        return fixtures
    for fixture_alias, fixture_name in marker.args[0].items():
        fixture = request.getfixturevalue(fixture_name)
        setattr(fixtures, fixture_alias, fixture)
    return fixtures
