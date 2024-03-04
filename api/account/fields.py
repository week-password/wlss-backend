from __future__ import annotations

from typing import Annotated

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core.core_schema import str_schema
from wlss.account.types import AccountEmail, AccountLogin, AccountPassword


AccountEmailField = Annotated[
    AccountEmail,
    PlainValidator(AccountEmail),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=AccountEmail.LENGTH_MAX.value,
            min_length=AccountEmail.LENGTH_MIN.value,
            pattern=AccountEmail.REGEXP.pattern,
        ),
    )),
]


AccountLoginField = Annotated[
    AccountLogin,
    PlainValidator(AccountLogin),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=AccountLogin.LENGTH_MAX.value,
            min_length=AccountLogin.LENGTH_MIN.value,
            pattern=AccountLogin.REGEXP.pattern,
        ),
    )),
]


AccountPasswordField = Annotated[
    AccountPassword,
    PlainValidator(AccountPassword),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=AccountPassword.LENGTH_MAX.value,
            min_length=AccountPassword.LENGTH_MIN.value,
        ),
    )),
]
