from __future__ import annotations

import json

import pydantic
import pytest

from api.auth.dtos import CreateSessionRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api"})
async def test(f):
    with pytest.raises(pydantic.ValidationError) as exc_info:
        await f.api.auth.create_session(
            request_data=CreateSessionRequest.model_validate({
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            }),
        )

    assert json.loads(exc_info.value.json()) == [
        {
            "type": "value_error",
            "loc": [],
            "msg": "Value error, You cannot use 'login' and 'email' together. Choose one of them.",
            "input": {
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            },
            "ctx": {
                "error": "You cannot use 'login' and 'email' together. Choose one of them.",
            },
            "url": "https://errors.pydantic.dev/2.5/v/value_error",
        },
    ]
