from __future__ import annotations

from typing import Annotated

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core.core_schema import str_schema
from wlss.wish.types import WishDescription, WishTitle


WishDescriptionField = Annotated[
    WishDescription,
    PlainValidator(WishDescription),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=WishDescription.LENGTH_MAX.value,
            min_length=WishDescription.LENGTH_MIN.value,
            pattern=WishDescription.REGEXP.pattern,
        ),
    )),
]


WishTitleField = Annotated[
    WishTitle,
    PlainValidator(WishTitle),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=WishTitle.LENGTH_MAX.value,
            min_length=WishTitle.LENGTH_MIN.value,
            pattern=WishTitle.REGEXP.pattern,
        ),
    )),
]
