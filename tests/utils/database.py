from __future__ import annotations

from sqlalchemy import text

from src.shared.database import sync_engine


def set_autoincrement_counters() -> None:
    """Set initial value for all auto-incremented sequences in db tables.

    This is needed to avoid conflicts between db objects created by fixtures
    and db objects created by the app itself.

    For example:
        fixture creates a new user with id = 1
        test calls application endpoint which will create another user
        since id column in fixtures was provided by hands, then
        autoincrement key is not switched to the next value and user created by
        application will have id = 1 as well. This will cause and error
        because application is trying to add a user with primary key which already exists.

    So this function just sets autoincrement counter for `id` columns in all database tables.
    """
    with sync_engine.connect() as connection:
        sequences = connection.execute(text("SELECT sequencename FROM pg_sequences;")).all()

    queries = ""
    for sequence_name, *_ in sequences:
        queries += f"ALTER SEQUENCE {sequence_name} RESTART WITH 10000;"

    # we avoid executing of empty query since this will give us an error from sqlalchemy
    if not queries:
        return

    with sync_engine.connect() as connection:
        connection.execute(text(queries))
        connection.commit()
