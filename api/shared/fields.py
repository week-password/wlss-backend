from __future__ import annotations

from datetime import datetime
from typing import Annotated, TYPE_CHECKING
from uuid import UUID

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core.core_schema import datetime_schema, int_schema, uuid_schema
from wlss.shared.types import Id, UtcDatetime

from api.shared.datetime import DATETIME_FORMAT


if TYPE_CHECKING:
    from typing import Any


def _validate_id(value: Any) -> Id:  # noqa: ANN401
    if isinstance(value, Id):
        value = value.value
    if isinstance(value, str):
        value = int(value)
    return Id(value)


IdField = Annotated[
    Id,
    PlainValidator(_validate_id),
    PlainSerializer(lambda v: v.value, return_type=int),
    WithJsonSchema(GenerateJsonSchema().generate(
        int_schema(
            ge=Id.VALUE_MIN.value,
        ),
    )),
]


def _validate_utcdatetime(value: Any) -> UtcDatetime:  # noqa: ANN401,SC200
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return UtcDatetime(value)


UtcDatetimeField = Annotated[
    UtcDatetime,
    PlainValidator(_validate_utcdatetime),  # noqa: SC200
    PlainSerializer(lambda v: v.value.strftime(DATETIME_FORMAT), return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        datetime_schema(
            tz_constraint="aware",
        ),
    )),
]


def _uuid_validator(value: Any) -> UUID:  # noqa: ANN401
    if isinstance(value, UUID):
        value = str(value)
    return UUID(value)


UuidField = Annotated[
    UUID,
    PlainValidator(_uuid_validator),
    PlainSerializer(lambda v: str(v), return_type=str),  # pylint: disable=unnecessary-lambda
    WithJsonSchema(GenerateJsonSchema().generate(
        uuid_schema(
            version=4,
        ),
    )),
]
