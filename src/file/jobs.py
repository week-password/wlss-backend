from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from sqlalchemy import delete, text

from src.config import CONFIG
from src.file.models import File
from src.shared.database import async_session
from src.shared.minio import Minio


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession


_DEFAULT_DB_SESSION: async_scoped_session[AsyncSession] = async_session


async def delete_unused_files(scoped_session: async_scoped_session[AsyncSession] = _DEFAULT_DB_SESSION) -> None:
    logger.info("Start deleting unused files")

    async with scoped_session() as session:
        query = text("""
            SELECT
                conrelid::regclass AS referencing_table,
                a.attname AS foreign_key_column
            FROM
                pg_constraint AS c
            JOIN
                pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
            WHERE
                confrelid = 'public.file'::regclass
            ;
        """)
        rows = (await session.execute(query)).all()

        unused_ids_query = f"""
            (
                SELECT
                    id as file_id
                FROM
                    {File.__tablename__}
                WHERE
                    created_at < ((NOW() AT TIME ZONE 'UTC') - interval '1 hour')
            )
        """
        logger.info("Will search for references to files in the following columns:")
        for table_name, column_name in rows:
            logger.info(f"    {table_name}.{column_name}")
            unused_ids_query += f"""
                EXCEPT (
                    SELECT
                        {table_name}.{column_name} AS file_id
                    FROM
                        {table_name}
                    WHERE
                        created_at < (
                            (NOW() AT TIME ZONE 'UTC')
                            - interval '{CONFIG.SCHEDULER_FILE_RETENTION_MINUTES_PERIOD} minutes'
                        )
                )
            """
        query = text(unused_ids_query + ";")
        file_ids = (await session.execute(query)).scalars().all()

        logger.info("Unused file ids found:")
        for file_id in file_ids:
            logger.info(f"    {file_id}")

        minio = Minio(
            CONFIG.MINIO_SCHEMA,
            CONFIG.MINIO_HOST,
            CONFIG.MINIO_PORT,
            CONFIG.MINIO_ROOT_USER,
            CONFIG.MINIO_ROOT_PASSWORD,
        )
        logger.info("Delete following files from minio:")
        for file_id in file_ids:
            logger.info(f"    {file_id}")
            minio.delete_file(file_id)

        logger.info("All unused files are deleted from MinIO.")

        query = delete(File).where(File.id.in_(file_ids)).returning(File)  # type: ignore[assignment]
        rows = (await session.execute(query)).all()

        logger.info("Following unused files are going to be deleted from database:")
        for row in rows:
            logger.info(f"    {row.File.id}")

        await session.commit()

        logger.info("Done.")
