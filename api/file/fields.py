from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core.core_schema import int_schema, str_schema
from wlss.file.types import FileName, FileSize


if TYPE_CHECKING:
    from typing import Any


FileNameField = Annotated[
    FileName,
    PlainValidator(FileName),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=FileName.LENGTH_MAX.value,
            min_length=FileName.LENGTH_MIN.value,
        ),
    )),
]


def _validate_file_size(value: Any) -> FileSize:  # noqa: ANN401
    if isinstance(value, FileSize):
        value = value.value
    return FileSize(value)


FileSizeField = Annotated[
    FileSize,
    PlainValidator(_validate_file_size),
    PlainSerializer(lambda v: v.value, return_type=int),
    WithJsonSchema(GenerateJsonSchema().generate(
        int_schema(
            ge=FileSize.VALUE_MIN.value,
            le=FileSize.VALUE_MAX.value,
        ),
    )),
]
