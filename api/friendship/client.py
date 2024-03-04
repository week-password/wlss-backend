from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.friendship.dtos import (
    AcceptFriendshipRequestResponse,
    CreateFriendshipRequestResponse,
    GetAccountFriendshipsResponse,
    GetFriendshipRequestsResponse,
    RejectFriendshipRequestResponse,
)


if TYPE_CHECKING:
    from typing import Self

    from wlss.shared.types import Id

    from api.friendship.dtos import CreateFriendshipRequestRequest


class Friendship:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_account_friendships(self: Self, account_id: Id, token: str) -> GetAccountFriendshipsResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/{account_id.value}/friendships",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetAccountFriendshipsResponse.model_validate(response.json())

    async def create_friendship_request(
        self: Self,
        request_data: CreateFriendshipRequestRequest,
        token: str,
    ) -> CreateFriendshipRequestResponse:
        async with self._client as client:
            response = await client.post(
                "/friendships/requests",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateFriendshipRequestResponse.model_validate(response.json())

    async def cancel_friendship_request(self: Self, request_id: Id, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/friendships/requests/{request_id.value}",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT

    async def accept_friendship_request(self: Self, request_id: Id, token: str) -> AcceptFriendshipRequestResponse:
        async with self._client as client:
            response = await client.put(
                f"/friendships/requests/{request_id.value}/accepted",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        return AcceptFriendshipRequestResponse.model_validate(response.json())

    async def reject_friendship_request(self: Self, request_id: Id, token: str) -> RejectFriendshipRequestResponse:
        async with self._client as client:
            response = await client.put(
                f"/friendships/requests/{request_id.value}/rejected",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return RejectFriendshipRequestResponse.model_validate(response.json())

    async def get_friendship_requests(self: Self, account_id: Id, token: str) -> GetFriendshipRequestsResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/{account_id.value}/friendships/requests",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetFriendshipRequestsResponse.model_validate(response.json())

    async def delete_friendships(self: Self, account_id: Id, friend_id: Id, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/accounts/{account_id.value}/friendships/{friend_id.value}",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT
