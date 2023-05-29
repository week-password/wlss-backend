"""Database utilities."""

from __future__ import annotations

from sqlalchemy import text

from src.shared.database import async_engine, Base


async def set_autoincrement_counters() -> None:
    """Set initial value for all auto-incremented sequences in db tables.

    This is needed to avoid conflicts between rows created by fixtures
    and values created by the app itself.

    For example:
        fixture creates a new user with id = 1
        test calls application endpoint which will create another user
        since id column in fixtures was provided by hands, then
        autoincrement key is not switched to the next value and user created by
        application will have id = 1 as well. This will cause and error
        because application is trying to add a user with primary key which already exists.

    So this function just sets autoincrement counter for `id` columns in all database tables.
    """
    queries = ""
    for tablename in Base.metadata.tables:
        queries += f"ALTER SEQUENCE {tablename}_id_seq RESTART WITH 10000;"  # pylint: disable=consider-using-join
    async with async_engine.connect() as connection:
        await connection.execute(text(queries))
