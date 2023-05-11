import asyncio
import importlib
import re
from logging.config import fileConfig

from alembic import context
from alembic.script import write_hooks
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.shared.database import Base, POSTGRES_CONNECTION_URL


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", POSTGRES_CONNECTION_URL)


# import models defined in `models_packages` in `alembic.ini` file
# this is needed to allow alembic identify existing models
# to be able to create migrations
models_packages = config.get_main_option("models_packages", None)
if models_packages is not None:
    PYTHON_PACKAGE_REGEX = r"([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)"
    matches = re.findall(PYTHON_PACKAGE_REGEX, models_packages)
    for module_path, _ in matches:
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            msg = f"Cannot import module `{e.name}`. Please check `models_packages` in `alembic.ini`."
            raise ImportError(msg) from None


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(
        config.config_file_name,
        disable_existing_loggers=False,  # will allow us to use `caplog` fixture in our tests without any issues
    )

# MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine and associate a connection with the context."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


@write_hooks.register("check_empty_migration")
def check_empty_migration(revision_path, options):
    from pathlib import Path
    from textwrap import dedent

    MIGRATIONS_DIR = Path(__file__).parent

    migration_files = list(MIGRATIONS_DIR.glob("versions/*.py"))

    with migration_files[-1].open() as f:
        empty_upgrade = dedent(
            """
            def upgrade() -> None:
                # ### commands auto generated by Alembic - please adjust! ###
                pass
                # ### end Alembic commands ###
            """
        )
        empty_downgrade = dedent(
            """
            def downgrade() -> None:
                # ### commands auto generated by Alembic - please adjust! ###
                pass
                # ### end Alembic commands ###
            """
        )
        migration_file = f.read()
        if empty_upgrade in migration_file and empty_downgrade in migration_file:
            print(
                dedent(
                    """
                    You've created an empty migration file.

                    Maybe you forgot to register your model in alembic.ini config?
                    Double check 'models_packages' option in configuration file.
                    """
                )
            )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
