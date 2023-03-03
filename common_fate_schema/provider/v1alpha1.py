import typing
from pydantic import BaseModel, Field


class TargetField(BaseModel):
    type: typing.Literal["string"]  # only string types supported for the moment
    title: typing.Optional[str]
    description: typing.Optional[str]
    resource: typing.Optional[str] = Field(
        description="If specified, the type of the resource the field should be populated from."
    )


class Target(BaseModel):
    type: typing.Literal["object"] = Field(
        description="included for compatibility with JSON Schema - all targets are currently objects."
    )
    properties: typing.Dict[str, TargetField] = Field(
        description="the actual properties of the target."
    )


class Meta(BaseModel):
    framework: str = Field(
        description="The Provider Developer Kit framework version which published the schema."
    )


class Loader(BaseModel):
    """
    A callable function in the provider which can
    load resources.

    Additional fields for loader configuration may be added
    in a future specification.
    """

    title: str


class Resources(BaseModel):
    loaders: typing.Dict[str, Loader]
    types: typing.Dict[str, typing.Any] = Field(description="the types of resources")


class Config(BaseModel):
    type: typing.Literal["string"]  # only string types supported for the moment
    description: str = Field(description="The usage for the config variable.")
    secret: bool


class Schema(BaseModel):
    """
    The schema for a Common Fate Provider.
    """

    targets: typing.Dict[str, Target]
    config: typing.Dict[str, typing.Any]
    resources: Resources
    meta: Meta

    class Config:
        schema_extra = {
            "$schema": "https://schema.commonfate.io/provider/v1alpha1",
            "$id": "https://schema.commonfate.io/provider/v1alpha1",
        }
