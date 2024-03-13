from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.file.constants import MEGABYTE
from api.file.dtos import CreateFileResponse, GetFileResponse


if TYPE_CHECKING:
    from pathlib import Path
    from typing import Self
    from uuid import UUID

    from api.file.dtos import CreateFileRequest


class File:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_file(self: Self, request_data: CreateFileRequest, token: str) -> CreateFileResponse:
        with request_data.tmp_file_path.open("rb") as f:

            response = await self._client.post(
                "/files",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (request_data.name, f, request_data.mime_type.value)},
            )

        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateFileResponse.model_validate(response.json())

    async def get_file(self: Self, file_id: UUID, tmp_file_path: Path) -> GetFileResponse:
        async with self._client.stream("GET", f"/files/{file_id}") as response:
            if response.is_error:
                await response.aread()
                response.raise_for_status()
            assert response.status_code == httpx.codes.OK
            with tmp_file_path.open("wb") as f:
                async for chunk_data in response.aiter_bytes(chunk_size=5 * MEGABYTE):
                    f.write(chunk_data)
        return GetFileResponse(
            path=tmp_file_path,
            status_code=response.status_code,
            media_type=response.headers["Content-Type"],
        )
