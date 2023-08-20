"""Database connection related stuff."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import CONFIG


if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from typing import Final

    from sqlalchemy.ext.asyncio import AsyncSession


# constants below are defined only for shortening long names from config
# they are not supposed to be used anywhere except this file
# that's why they have leading underscores in their names
_DB: Final = CONFIG.POSTGRES_DB
_HOST: Final = CONFIG.POSTGRES_HOST
_PASSWORD: Final = CONFIG.POSTGRES_PASSWORD
_PORT: Final = CONFIG.POSTGRES_PORT
_USER: Final = CONFIG.POSTGRES_USER


POSTGRES_CONNECTION_URL: Final = f"postgresql+asyncpg://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_DB}"
POSTGRES_CONNECTION_URL_SYNC: Final = f"postgresql+psycopg2://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_DB}"

# will allow us to connect to the database
async_engine = create_async_engine(POSTGRES_CONNECTION_URL)
sync_engine = create_engine(POSTGRES_CONNECTION_URL_SYNC)  # needed for some cases when we cannot use async python code

# will allow us to send SQL queries to database associated with engine
async_session = async_scoped_session(async_sessionmaker(bind=async_engine), scopefunc=asyncio.current_task)


# will allow us to map relation tables from PostgreSQL to python classes
# each model must inherit this Base class
class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base class for models."""


async def get_session() -> AsyncIterator[AsyncSession]:  # pragma: no cover
    """Get database session. FastAPI dependency for database session."""
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()
