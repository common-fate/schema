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
    framework: typing.Optional[str] = Field(
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
    description: typing.Optional[str] = Field(
        description="The usage for the config variable."
    )
    secret: bool = False


class Provider(BaseModel):
    publisher: str
    name: str
    schema_version: str
    """
    The version of the schema (*not* the version of the Provider itself).
    """


class Schema(BaseModel):
    """
    The schema for a Common Fate Provider.
    """

    provider: typing.Optional[Provider] = Field(exclude=True)
    targets: typing.Dict[str, Target]
    config: typing.Dict[str, Config]
    resources: Resources
    meta: Meta

    def dict(self, *args, **kwargs):
        self.__dict__.update(
            {
                "$schema": "https://schema.commonfate.io/provider/v1alpha1",
            }
        )

        if self.provider is not None:
            self.__dict__.update(
                {
                    "$id": f"https://registry.commonfate.io/schema/{self.provider.publisher}/{self.provider.name}/{self.provider.schema_version}",
                }
            )

        return super().dict(*args, **kwargs)

    def json(
        self,
        *args,
        **kwargs,
    ) -> str:
        self.__dict__.update(
            {
                "$schema": "https://schema.commonfate.io/provider/v1alpha1",
            }
        )

        if self.provider is not None:
            self.__dict__.update(
                {
                    "$id": f"https://registry.commonfate.io/schema/{self.provider.publisher}/{self.provider.name}/{self.provider.schema_version}",
                }
            )

        super().json(*args, **kwargs)

    class Config:
        schema_extra = {
            "$schema": "https://schema.commonfate.io/provider/v1alpha1",
            "$id": "https://schema.commonfate.io/provider/v1alpha1",
        }
