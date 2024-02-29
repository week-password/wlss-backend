from __future__ import annotations

from typing import Annotated

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core.core_schema import str_schema
from wlss.profile.types import ProfileDescription, ProfileName


ProfileDescriptionField = Annotated[
    ProfileDescription,
    PlainValidator(ProfileDescription),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=ProfileDescription.LENGTH_MAX.value,
            min_length=ProfileDescription.LENGTH_MIN.value,
            pattern=ProfileDescription.REGEXP.pattern,
        ),
    )),
]


ProfileNameField = Annotated[
    ProfileName,
    PlainValidator(ProfileName),
    PlainSerializer(lambda v: v.value, return_type=str),
    WithJsonSchema(GenerateJsonSchema().generate(
        str_schema(
            max_length=ProfileName.LENGTH_MAX.value,
            min_length=ProfileName.LENGTH_MIN.value,
            pattern=ProfileName.REGEXP.pattern,
        ),
    )),
]
